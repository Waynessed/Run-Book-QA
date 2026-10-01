import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import recorded from './recorded-demo.json';
import './style.css';

type Passage = {id:string; document_id:string; title:string; version:string; heading:string; section_id:string; text:string};
type Answer = {status:string; claims:{text:string; citation_ids:string[]}[]; reason:string; passages:Passage[]; latency_ms:number; retrieval_mode:string; model_version:string; corpus_version:string};
type Source = {title:string; version:string; markdown:string};
const recordedMode = import.meta.env.VITE_RECORDED_DEMO === '1';
const liveSamples = [
  'The API returns 401 after deployment. What should I check?',
  'Why is the container restarting?',
  'How do I investigate exhausted database connections?',
  'How do I roll back a deployment?',
  'When should I escalate an incident?',
  'What is the office Wi-Fi password?',
  'How do I configure payroll taxes?',
];
const samples = recordedMode ? Array.from(new Set(recorded.examples.map(item => item.question))) : liveSamples;

function App() {
  const [question, setQuestion] = useState(samples[0]);
  const [mode, setMode] = useState('hybrid');
  const [answer, setAnswer] = useState<Answer|null>(null);
  const [review, setReview] = useState<(typeof recorded.examples)[number]['review']|null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [ready, setReady] = useState(recordedMode ? 'Recorded development responses' : 'Checking local services…');
  const [source, setSource] = useState<Source|null>(null);
  const [selected, setSelected] = useState<Passage|null>(null);
  const [report, setReport] = useState<any>(recordedMode ? {split:recorded.evaluation.split, rows:{length:recorded.evaluation.row_count}, modes:recorded.evaluation.modes} : null);

  useEffect(() => {
    if (recordedMode) return;
    fetch('/readyz').then(async response => {
      const body = await response.json();
      setReady(response.ok ? 'Local model and corpus ready' : String(body.detail));
    }).catch(() => setReady('API unavailable. Run scripts/bootstrap.ps1.'));
    fetch('/v1/evaluation/latest').then(response => response.json()).then(setReport).catch(() => {});
  }, []);

  async function submit(event:React.FormEvent) {
    event.preventDefault();
    setError(''); setAnswer(null); setReview(null); setSource(null); setSelected(null);
    if (recordedMode) {
      const item = recorded.examples.find(example => example.question === question && example.mode === mode);
      if (!item) {
        setError('This preview contains only the listed recorded questions and modes. Run the project locally to ask a new question.');
        return;
      }
      setAnswer(item.answer);
      setReview(item.review);
      return;
    }
    setBusy(true);
    try {
      const response = await fetch('/v1/ask', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({question, retrieval_mode:mode})});
      const body = await response.json();
      if (!response.ok) throw Error(typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail));
      setAnswer(body);
    } catch (failure) { setError(String(failure)); }
    finally { setBusy(false); }
  }

  async function open(passage:Passage) {
    setSelected(passage); setSource(null);
    if (recordedMode) {
      const document = recorded.documents[passage.document_id as keyof typeof recorded.documents];
      if (document) setSource(document);
      else setError('Recorded source unavailable.');
      return;
    }
    try {
      const response = await fetch('/v1/documents/' + encodeURIComponent(passage.document_id));
      if (!response.ok) throw Error('Source unavailable');
      setSource(await response.json());
    } catch (failure) { setError(String(failure)); }
  }

  return <main>
    <header><a className="brand" href={import.meta.env.BASE_URL}>RunbookQA<span>Support workbench</span></a><span className="health">{ready}</span></header>
    {recordedMode && <aside className="preview-notice"><strong>Recorded recruiter preview</strong><span>These are saved responses from a real local Qwen development run. Select a listed question and retrieval mode to inspect the recorded answer and original source. This static page does not generate new answers. <a href="https://github.com/Waynessed/Run-Book-QA">View the code and local setup</a>.</span></aside>}
    <section className="intro"><h1>Find the next check.<br/>Keep the evidence close.</h1><p>Ask about the fictional Northstar services. Answers reference the indexed runbooks, with each source available to inspect.</p></section>
    <div className="workspace">
      <section className="question"><form onSubmit={submit}><label htmlFor="question">What are you investigating?</label><textarea id="question" maxLength={1000} value={question} readOnly={recordedMode} onChange={event=>setQuestion(event.target.value)} required/><div className="actions"><label>Retrieval <select aria-label="Retrieval mode" value={mode} onChange={event=>setMode(event.target.value)}><option value="keyword">Keyword</option><option value="semantic">Semantic</option><option value="hybrid">Hybrid + reranking</option></select></label><button disabled={busy}>{busy?'Reading evidence…':recordedMode?'Show recorded answer':'Ask runbooks'}</button></div></form><details className="samples" open><summary>{recordedMode?'Recorded questions':'Try a question'}</summary>{samples.map(sample=><button key={sample} onClick={()=>{setQuestion(sample);setAnswer(null);setReview(null);setSource(null);setSelected(null);}}>{sample}</button>)}</details></section>
      <section className="result" aria-live="polite"><h2>{answer?.status==='abstained'?'Insufficient evidence':'Answer'}</h2>{busy&&<p>Retrieving passages and waiting for the local model. CPU generation can take up to 120 seconds per attempt.</p>}{error&&<p role="alert" className="error">{error}</p>}{!answer&&!busy&&!error&&<p className="empty">{recordedMode?'Choose a recorded question and mode to inspect a saved output.':'Your answer and source passages will appear here.'}</p>}{answer&&<><p>{answer.reason}</p>{answer.claims.map((claim,index)=><article className="claim" key={index}><p>{claim.text}</p>{claim.citation_ids.map(id=>{const passage=answer.passages.find(item=>item.id===id);return passage?<button className="citation" key={id} onClick={()=>open(passage)}>{passage.title} / {passage.heading} · v{passage.version}</button>:null;})}</article>)}<p className="meta">{answer.retrieval_mode} · {(answer.latency_ms/1000).toFixed(1)} seconds {recordedMode?'in the saved development run':''}</p>{review&&<p className="review-note">Recorded source inspection: fact score {review.fact_correctness}; {review.supported_claims}/{review.claim_count} claims supported. {review.notes}</p>}<details><summary>Run metadata</summary><small>Model: {answer.model_version}<br/>Corpus: {answer.corpus_version}{recordedMode&&<><br/>Development report: {recorded.source_report}<br/>Git: {recorded.source_git_commit}</>}</small></details><h3>Retrieved evidence</h3>{answer.passages.map(passage=><details key={passage.id}><summary>{passage.title} / {passage.heading} · v{passage.version}</summary><p>{passage.text}</p><button onClick={()=>open(passage)}>Open source section</button></details>)}</>}</section>
    </div>
    {selected&&<section className="source" id={selected.section_id}><button className="close" onClick={()=>{setSource(null);setSelected(null);}}>Close source</button><h2>{selected.title} / {selected.heading}</h2><p>Retrieved document version {selected.version}</p><blockquote>{selected.text}</blockquote>{source?<details open><summary>Full current document · v{source.version}</summary>{source.version!==selected.version&&<p>The source has been updated since this answer.</p>}<pre>{source.markdown}</pre></details>:<p>Loading source…</p>}</section>}
    <section className="evaluation"><h2>Retrieval comparison</h2>{report?.modes?<><p>Measured {report.split} run · {report.rows?.length ?? 'unknown'} recorded outputs. Fact scores cover all labelled cases; claim support counts only generated claims. {recordedMode&&'These metrics belong to the original frozen held-out revision, separate from the selected development examples.'}</p><table><thead><tr><th>Mode</th><th>Recall@5</th><th>Fact score</th><th>Claim support</th><th>Unsupported abstention</th><th>Answerable coverage</th><th>p95 latency</th></tr></thead><tbody>{Object.entries(report.modes).map(([key,metrics]:[string,any])=><tr key={key}><td>{key}</td><td>{(metrics.recall_at_5*100).toFixed(1)}%</td><td>{metrics.answer_correctness==null?'Unreviewed':(metrics.answer_correctness*100).toFixed(1)+'%'}</td><td>{metrics.supported_claim_rate==null?'Unreviewed':(metrics.supported_claim_rate*100).toFixed(1)+'%'}</td><td>{(metrics.unsupported_abstention*100).toFixed(1)}%</td><td>{(metrics.answerable_coverage*100).toFixed(1)}%</td><td>{(metrics.p95_latency_ms/1000).toFixed(1)}s</td></tr>)}</tbody></table><p className="review-provenance">{Object.values(report.modes).every((metrics:any)=>metrics.semantic_review_status==='reviewed')?'Semantic inspection: '+Object.values(report.modes).map((metrics:any)=>metrics.reviewer).filter((value,index,array)=>array.indexOf(value)===index).join('; '):'Semantic correctness and claim support await recorded rubric review.'}</p><table aria-label="Validation and failures"><thead><tr><th>Mode</th><th>Valid citation IDs</th><th>Adversarial instruction failures</th><th>Rejected directives</th><th>Model errors</th><th>Median latency</th></tr></thead><tbody>{Object.entries(report.modes).map(([key,metrics]:[string,any])=><tr key={key}><td>{key}</td><td>{metrics.valid_citation_rate==null?'No citations':(metrics.valid_citation_rate*100).toFixed(1)+'%'}</td><td>{metrics.adversarial_instruction_failures==null?'Unreviewed':metrics.adversarial_instruction_failures}</td><td>{metrics.policy_rejection_attempts==null?'Not recorded':metrics.policy_rejection_attempts}</td><td>{metrics.model_errors}</td><td>{(metrics.median_latency_ms/1000).toFixed(1)}s</td></tr>)}</tbody></table><p className="meta">Valid citation IDs identify supplied passages; semantic support is scored separately. Rejected directives count a narrow text validator. Marker checks alone do not establish instruction resistance.</p></>:<p>No evaluation has been run yet. This table will show saved measurements when available.</p>}</section>
    <footer>Fictional corpus · {recordedMode?'Recorded local inference':'Local inference'} · Check supporting evidence before acting</footer>
  </main>;
}

createRoot(document.getElementById('root')!).render(<App/>);
