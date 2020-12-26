# Converter from FASTQ to FASTA
# Student Code Number : 844659
# Name : Simone
# Surname : Mallei

from Bio import SeqIO
import re

# Returns the minimum quality value in read
def get_min_quality(read):
    return min(read.letter_annotations['phred_quality'])

# Returns the longest subregion
# with minimum_quality >= quality_threshold
def get_quality_subregion(read, quality_threshold):
    quality_list = read.letter_annotations['phred_quality']
    available_list = [quality >= quality_threshold for quality in quality_list]
    start, end = 0, -1
    curr_start, curr_end = -1, -1
    interval_found = False
    for i in range(len(available_list)):
        if available_list[i]:
            if not(interval_found):
                curr_start = i
                interval_found = True
            curr_end = i
        elif curr_start != -1:
            # Checks if the new interval that has been found is the
            # longest subregion in the range [0,i]
            if end - start < curr_end - curr_start:
                start, end = curr_start, curr_end
            interval_found = False
            curr_start, curr_end = -1, -1
    if curr_start != -1 and end - start >= curr_end - curr_start:
        start, end = curr_start, curr_end
    return (start, end)


# Returns the average quality of the read in the
# subregion denoted by [interval[0], interval[1]]
def get_medium_quality(read, interval):
    quality_list = read.letter_annotations['phred_quality'][interval[0]:interval[1]+1]
    return sum(quality_list) / len(quality_list)

# Returns the percentual length (100% -> 1.0) of the longest subregion
# with minimum_quality >= quality_threshold
def get_quality_percentage(read, quality_threshold):
    interval = get_quality_subregion(read, quality_threshold)
    return (interval[1] - interval[0] + 1) / len(read.seq)

# Adds in the read's description the following attributes
# seq_length = length of the read's sequence
# min_quality = minimum read's quality value 
# start_subregion = start of the read's longest subregion with min_quality >= Q2
# end_subregion = end of the read's longest subregion with min_quality >= Q2
# avg_quality_subregion = average of read's quality value in its longest 
#                         subregion with min_quality >= Q2
def convert_read(read, Q2):
    min_quality = get_min_quality(read)
    interval = get_quality_subregion(read, Q2)
    read.description = '/seq_length=' + str(len(read.seq))
    read.description += ' /min_quality=' + str(min_quality)
    read.description += ' /start_subregion=' + str(interval[0])
    read.description += ' /end_subregion=' + str(interval[1])
    read.description += ' /avg_quality_subregion=' + str(get_medium_quality(read, interval))
    return read

# Converts list of reads to another list containing only reads
# that do not violate the constraints, adds infos in the description attribute
def convert(reads_list, L1, L2, Q1, Q2, P):
    # Read's length must be between L1 and L2
    reads_list = [read for read in reads_list if L1 <= len(read.seq) <= L2]
    
    # Read's minimum quality value must be greater than Q1
    reads_list = [read for read in reads_list if get_min_quality(read) > Q1]
    
    # The percentual length of the longest subregion with minimum_quality >= Q2
    # of each read must be >= P%
    reads_list = [read for read in reads_list if get_quality_percentage(read, Q2) >= P]
    
    converted_list = []
    for read in reads_list:
        converted_list.append(convert_read(read, Q2))
    return converted_list

# Main
if __name__ == "__main__":
    try:
        # Input from stdin
        print("Insert the name of the file .fq you want to convert to .fasta: ")
        fastq_file_name = input()
        print("Insert the value of L1: ")
        L1 = int(input())
        print("Insert the value of L2 (must be > L1): ")
        L2 = int(input())
        while (L2 <= L1):
            print("L2 is not greater than L1, insert again L2: ")
            L2 = int(input())
        print("Insert the value of Q1: ")
        Q1 = int(input())
        print("Insert the value of Q2 (must be > Q1): ")
        Q2 = int(input())
        while (Q2 <= Q1):
            print("Q2 is not greater than Q1, insert again Q2: ")
            Q2 = int(input())
        print("Insert the value of P (100% -> 1.0, 50% -> 0.5): ")
        P = float(input())

        # Reading the .fq file        
        fastq_records = SeqIO.parse(fastq_file_name, 'fastq')
        reads_list = [read for read in fastq_records]
        # Converting the reads
        converted_list = convert(reads_list, L1, L2, Q1, Q2, P)
        # Writing the converted records in fasta's format
        for read in converted_list:
            print(read.format('fasta'))
        file_name = re.findall('(\w*).fq', fastq_file_name)[0]
        SeqIO.write(converted_list, file_name + '.fa', 'fasta')
    except:
        print('Error during the execution of the converter, restart the file.')
