export interface Agency {
  name: string;
  title?: string;
  tagline?: string;
  category?: string;
  agents?: number;
  tools?: number;
  max_cost_usd?: number;
  self_improving?: boolean;
  path: string;
}

export interface Company {
  name: string;
  title?: string;
  positioning?: string;
  node_count?: number;
  member_agencies?: string[];
  members?: (string | { name?: string; title?: string })[];
}

export interface BenchmarkQuality {
  memory_corrected_pct?: number;
  control_corrected_pct?: number;
  memory_raw_pct?: number;
  control_raw_pct?: number;
  memory_n?: number;
  control_n?: number;
}

export interface BenchmarkCost {
  clean_pairs?: number;
  memory_cheaper_pairs?: number;
  mean_delta_usd?: number;
  sign_test_p?: number;
  verdict?: string;
}

export interface BenchmarkRecord {
  subject_type?: string;
  subject?: string;
  benchmark?: string;
  date?: string;
  fabri_version?: string;
  roster_revision?: string | null;
  replicas?: number;
  quality?: BenchmarkQuality;
  cost?: BenchmarkCost;
  control_memory_free?: boolean;
  excluded_arms?: number;
  spend_usd?: number;
  report_url?: string;
}

export interface Benchmarks {
  schema_version?: number;
  generated_at?: string;
  headline?: string;
  records?: BenchmarkRecord[];
}

export interface Catalog {
  agencies: Agency[];
  companies?: Company[];
  benchmarks?: Benchmarks;
}
