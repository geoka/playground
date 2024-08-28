from langchain_google_community import BigQueryLoader

# A document loader for BigQuery
# Uses default credentials / Application Default Credentials. 
# 
# 1: Set up Application Default Credentials: for local dev (preferred) or identity provider 
# Ref: https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to
# Ensure gcloud auth application-default set-quota-project PROJECT_ID &  gcloud config set project PROJECT_ID
# 2: Load data
# Ref: https://python.langchain.com/v0.2/docs/integrations/document_loaders/google_bigquery/



BASE_QUERY = """
SELECT
  id,
  dna_sequence,
  organism
FROM (
  SELECT
    ARRAY (
    SELECT
      AS STRUCT 1 AS id, "ATTCGA" AS dna_sequence, "Lokiarchaeum sp. (strain GC14_75)." AS organism
    UNION ALL
    SELECT
      AS STRUCT 2 AS id, "AGGCGA" AS dna_sequence, "Heimdallarchaeota archaeon (strain LC_2)." AS organism
    UNION ALL
    SELECT
      AS STRUCT 3 AS id, "TCCGGA" AS dna_sequence, "Acidianus hospitalis (strain W1)." AS organism) AS new_array),
  UNNEST(new_array)
"""
# Specifying Which Columns are Content vs Metadata
loader = BigQueryLoader(
    BASE_QUERY,
    page_content_columns=["dna_sequence", "organism"],
    metadata_columns=["id"],
)
# loader = BigQueryLoader(BASE_QUERY)

data = loader.load()

print(data)

