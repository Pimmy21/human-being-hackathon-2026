// Application adapter, not a reimplementation of Meterless H-MEM.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

try {
  const request = JSON.parse(fs.readFileSync(0, 'utf8'));
  const validId = x => typeof x === 'string' && /^[a-zA-Z0-9_-]{1,64}$/.test(x);
  if (!validId(request.workspace) || !validId(request.case_id)) throw Error('Invalid scope');
  if (!path.isAbsolute(request.state_root) || !path.isAbsolute(request.reference)) throw Error('Absolute configured paths required');
  const { HMEM } = await import(pathToFileURL(request.reference).href);
  // Separate stores plus exact scope filtering; do not rely solely on chatId.
  const persistDir = path.join(request.state_root, request.workspace, request.case_id);
  const hmem = new HMEM({ persistDir, actor: 'purrpose-local-demo' });
  const scope = `${request.workspace}:${request.case_id}`;
  const total = hmem.store.all().length;
  if (total > 500) throw Error('Demo memory capacity reached');
  const recalled = hmem.query(`Purrpose ${request.case_id} evidence grant funding unresolved`, {
    chatId: scope, threshold: 0, topN: Math.max(1, total),
  });
  // Threshold 0 deliberately retrieves the bounded full case snapshot history.
  // Hybrid scores are returned, but are not used as truth or chronological order.
  const entries = recalled.memories.filter(x => x.memory.chatId === scope
    && x.memory.tags.includes(`case:${request.case_id}`)).map(x => ({
      memory_id: x.memory.id, relevance: x.relevance,
      system_recorded_at: new Date(x.memory.timestamp).toISOString(),
      payload: JSON.parse(x.memory.content),
    })).filter(x => x.payload.case_id === request.case_id);
  entries.sort((a, b) => Number(b.memory_id.replace('mem-', '')) - Number(a.memory_id.replace('mem-', '')));
  if (request.op === 'recall') {
    console.log(JSON.stringify({ entries, trace: recalled.trace, engine: 'official_hmem_reference' }));
  } else if (request.op === 'save') {
    const p = request.payload;
    if (!p || p.case_id !== request.case_id || p.schema_version !== 1 || !p.run_id
        || !Array.isArray(p.source_refs) || !p.source_refs.length) throw Error('Invalid sourced snapshot');
    const existing = entries.find(x => x.payload.run_id === p.run_id);
    const previous = entries[0];
    const isReal = p.scenario_type === 'real_public_observations';
    const memory = existing ? {id: existing.memory_id} : hmem.add({
      content: JSON.stringify(p), type: 'factual', layer: 'working', confidence: 1,
      source: p.source_refs.join(' '), chatId: scope,
      provenance: {origin: 'document', learnedAt: Date.now(),
        label: `${isReal ? 'Real public observation' : 'Synthetic evidence'} review snapshot; confidence describes capture, not real-world trust`,
        refs: p.source_refs},
      tags: [`case:${request.case_id}`, 'purrpose-review', isReal ? 'real-public-observations' : 'synthetic'],
      supersedes: previous?.memory_id,
    });
    console.log(JSON.stringify({memory_id: memory.id, reused: Boolean(existing),
      supersedes: previous?.memory_id ?? null, engine: 'official_hmem_reference'}));
  } else throw Error('Unsupported operation');
} catch {
  // Do not emit user payloads, local paths or raw upstream errors.
  console.error('H-MEM operation failed: inspect configured runtime, scope, reference and local state');
  process.exitCode = 1;
}
