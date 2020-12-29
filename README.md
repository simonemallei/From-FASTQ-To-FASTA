# From-FASTQ-To-FASTA
Converter from .fq to .fa

Input:
- **fastq_file_name**: the path to the .fq file containing the reads to convert
- **L1**: Minimum length of the sequence in each read
- **L2**: Maximum length of the sequence in each read (> *L1*)
- **Q1**: Lower bound of the minimum quality in each read
- **Q2**: Lower bound of the minimum quality of the subregion considered (> *Q1*)
- **P**: Lower bound for the percentage of the length of the subregion / length of the entire sequence (*P* goes from 0.0 to 1.0, so 10% -> 0.1, 5% -> 0.05...)

Output:
- **fasta_file**: it contains the reads (that verify the constraints) converted in .fa format, it will be in the same position of *fastq_file_name* (it has .fa extension instead of .fq)


Each read, in order to be converted, has to verify these conditions:
- Its sequence's length has to be >= *L1* and <= *L2*
- Its minimum quality has to be >= *Q1*
- The length of the longest subregion of the sequence with minimum_quality >= *Q2* divided by the length of the entire sequence has to be >= *P*

For each read, the FASTA's header will have the following information:
- ID
- Length
- Minimum Quality
- Start index of the longest subregion with minimum quality >= *Q2*
- End index of the longest subregion with minimum quality >= *Q2*
- Average quality of the longest subregion with minimum quality >= *Q2*

Samples:
In 'samples/' there are some examples of possible .fq files converted in .fa files (the inputs are very similar), here the following values used to obtain the outputs:

| Sample File | L1 | L2 | Q1 | Q2 | P |
|-------------|----|----|----|----|---|
| sample0.fq | 10 | 50 | 40 | 60 | 0.3 (30%) |
| sample1.fq | 30 | 40 | 50 | 64 | 0.1 (10%) |
| sample2.fq | 36 | 36 | 55 | 59 | 0.6 (60%) |
| sample3.fq | 10 | 100 | 39 | 40 | 1.0 (100%) |
