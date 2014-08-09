enron-formality
===============

------------------------------------------------------
Results for 'Email Formality in the Workplace: A Case Study on the Enron Corpus'
URL for paper
http://aclweb.org/anthology-new/W/W11/W11-0711.pdf

Kelly Peterson
kellypet@uw.edu

Matt Hohensee
hohensee@uw.edu

Fei Xia 
fxia@uw.edu

------------------------------------------------------

Data references : 
ISI database : Retrieved December, 2010 from:
* http://www.isi.edu/˜adibi/Enron/Enron.htm
University of Sheffield personal vs business annotations : Retrieved December, 2010 from:
* http://staffwww.dcs.shef.ac.uk/people/L.Guthrie/nlp/research.htm
    
------------------------------------------------------

File Contents:
/README
    Dearest reader, you are reading me as we speak
/annotations/
    All of the human annotated files for formality and requests
    NOTE : when an email ends in .txt, this is numbered by the 'mid' column in the ISI database.  
    Otherwise, the filenames are the same as the originals from the CMU dataset
    /formality/
        /100_emails_agreement
            Initially, 3 annotators ennotated 100 emails for formality annotation agreement
        /400_emails_training
            After agreement, one annotator had time to annotate another 300 emails totalling 400 so that the classifier could be trained
    /requests/
        2 annotators annotated for the presence of a request.  
        In these files, a '1' right of the file name indicates a request, otherwise there was no request
/mysql/
    /queries/
        /get_formality_and_requests_by_position.sql
            This query was used to derive the results in Table 6 of the paper
        /get_formality_by_rank_diff.sql
            This query was used to derive the results in Table 7 of the paper
        /requests_and_formality.sql
            This query was used to derive the results in Table 8 of the paper
        /get_recipient_count_and_formality.sql
            This query was used to derive the results in Table 9 of the paper
    /tables/
        3 tables were added to the ISI database during our case study.  All of these can be used to JOIN against MySQL tables provided by ISI.
        No indexing is added to any of the columns in these .sql so please note that queries will run EXTREMELY slowly until indexing is added.  
        You will likely want to add an INDEX to the following columns : 'mid', 'Address' and 'Rank'
        /enron_formality.sql
            This table comprises the formality classification results in the column 'EffectiveLabel' (0=Empty, 1=Formal, 2=Informal)
            It also contains counts of the various features that the classifier extracted
        /enron_positions.sql
            A table created based on the positions in the ISI spreadsheet
        /enron_requests.sql
            This table comprises the requests classification results in the column 'RawLabel' (0=NonRequest, 1=Request)
/python/
    For more information on running these scripts or reproducing these results, please contact Kelly Peterson
    /contact_frequency/
        This script was used in combination with a CSV file exported from MySQL to derive the results in Table 5 of the paper
    /personal_vs_business_formality/
        This script was used in conjunction with Mallet's output from running against the 
        University of Sheffield Personal vs. Business dataset to derive the resul