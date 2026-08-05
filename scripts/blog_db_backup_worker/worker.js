// db-backup-export worker | 2026-06-02 by Claude Opus 4.8 for Max.
// Read-only JSON export of ALL Cloudflare D1 databases, behind a bearer token.
// Exists so the nightly/30-min backup can dump every site's source-of-truth DB
// without a D1-scoped API token (the workers/KV token returns 403 on D1).
// Bound to every D1 database; deployed separately on workers.dev so it never
// touches any live site. GET /            -> list of available db names
//                        GET /db/<name>   -> full JSON dump of that database
//
// Deploy: see deploy.sh in this folder (multipart PUT with all D1 bindings).

const SECRET = "blogbk_yDUsFeUxAAqosnMK4uhVp0sO1Mno0nnR";

// display name -> binding variable on env
const DBS = {
  "maxrempel-blog": "D_blog",
  "babel-db": "D_babel",
  "moma-db": "D_moma",
  "claude-memory-db": "D_memory",
  "starseed-genetics-contacts": "D_starseed",
  "cozy1": "D_cozy1",
  "cozy2": "D_cozy2",
  "cozy1_backup_20260118": "D_cozy1bak",
  "lizmasters1": "D_lizmasters1",
  "lizjobs1": "D_lizjobs1",
  "test_db_250107": "D_test",
};

async function dumpDb(db) {
  const t = await db.prepare(
    "SELECT name FROM sqlite_master WHERE type='table' " +
    "AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%' ORDER BY name"
  ).all();
  const out = { dumped_at: new Date().toISOString(), tables: {} };
  for (const row of t.results) {
    const r = await db.prepare(`SELECT * FROM ${row.name}`).all();
    out.tables[row.name] = r.results;
  }
  return out;
}

export default {
  async fetch(request, env) {
    if (request.headers.get("Authorization") !== `Bearer ${SECRET}`) {
      return new Response("forbidden", { status: 403 });
    }
    const url = new URL(request.url);
    if (url.pathname === "/" || url.pathname === "") {
      return Response.json({ databases: Object.keys(DBS) });
    }
    const m = url.pathname.match(/^\/db\/(.+)$/);
    if (m) {
      const name = decodeURIComponent(m[1]);
      const binding = DBS[name];
      if (!binding || !env[binding]) {
        return new Response("unknown db: " + name, { status: 404 });
      }
      try {
        const dump = await dumpDb(env[binding]);
        dump.db_name = name;
        return new Response(JSON.stringify(dump), {
          headers: { "Content-Type": "application/json" },
        });
      } catch (e) {
        return new Response("export error: " + e.message, { status: 500 });
      }
    }
    return new Response("not found", { status: 404 });
  },
};
