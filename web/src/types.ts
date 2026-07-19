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

export interface Catalog {
  agencies: Agency[];
  companies?: Company[];
}
