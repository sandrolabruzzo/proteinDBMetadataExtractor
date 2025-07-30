# Protein Database Metadata Extractor
This repository contains a set of scripts and tools designed to extract key metadata directly from the public FTP dumps of protein structures available at https://files.wwpdb.org/pub/pdb/data/structures/all/.

The primary goal of *ProteinDBMetadataExtractor* is to facilitate large-scale analysis of protein structural information by converting raw, often heterogeneous, Protein Data Bank (PDB) data into a more structured and easily queryable format. Specifically, these scripts start from the individual protein dump files and extract their metadata, conforming to a metadata schema.

# Use Cases
This tool is ideal for researchers, bioinformaticians, and developers who need to:

- Create local databases of PDB metadata.

- Perform complex searches based on structural and biological attributes.

- Support statistical analyses on protein datasets.

- Integrate PDB metadata into existing data analysis pipelines.


# MetaData Schema
This schema defines the structure for representing core metadata associated with an entry from the Protein Data Bank (PDB). Each instance of this schema captures key bibliographic and publication-related information for a specific PDB entry.

Fields:
- `pdb` (string) : The unique 4-character identifier for the PDB entry (e.g., "1XYZ"). This serves as the primary key for the record.

- `title` (string): The full title of the publication associated with the PDB entry. This typically describes the research work that led to the structure determination.

- `authors` (List of strings): A list of names of the authors who contributed to the publication associated with the PDB entry. Each element in the list represents an individual author's name.

- `doi` (string): The Digital Object Identifier (DOI) for the primary publication related to the PDB entry. This provides a persistent link to the article. Can be an empty string if not available.

- `pmid` (string): The PubMed ID (PMID) for the primary publication related to the PDB entry. This identifies the article in the PubMed database. Can be an empty string if not available.

- `date` (string): The deposition date of the PDB entry, typically in a standardized format (e.g., "YYYY-MM-DD"). This indicates when the structure was initially submitted to the PDB.

- `revDate` (List of RelevantDate objects): A list of revision dates for the PDB entry. Each element in the list is expected to be an instance of a RelevantDate class (which needs to be separately defined) that likely contains details about the revision, such as the date itself and potentially a description of the changes.


