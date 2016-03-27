

The Python script holidays_map.py computes the mean average precision
of a series of queries in the Holidays database. It is used like:

python holidays_map.py my_result_file.dat

Required
========

It needs the file holidays_images.dat to be in the current directory.

Python version >= 2.4 is needed.

Input file
==========

The mAP is computed from a result file in text. Its format (in sloppy
BNF) is:

result_file = ( result_line newline )*

# each line is a query image with associated results
result_line = query_image_name query_result*

# a query result is a pair: the result's filename is prefixed with its
# rank (0 based) 
query_result = rank result_image_name

Where:
- all items are separated by whitespaces (space or tab)
- image names are like 12345.jpg (case sensitive)
- the order of queries is not relevant
- if the query image is ranked, it is ignored in the scoring

The format was chosen to be compact and readable by a human. 

Examples
========

There are a few example result files: 

- perfect_result.dat is a perfect result file computed from the ground
truth

- baseline_result_200806.dat and he_wgc_result_200806.dat are output
by our indexing system. The results from the article are from these
datafiles.

This is a sample mAP computation:

eval_holidays $ python holidays_map.py perfect_result.dat
mAP for perfect_result.dat: 1.00000

eval_holidays $ python holidays_map.py he_wgc_result_200806.dat
mAP for he_wgc_result_200806.dat: 0.74626


References
==========

Where to download the Holidays dataset:

http://lear.inrialpes.fr/~jegou/data.php

The paper that presents it:

Herve Jegou, Matthijs Douze and Cordelia Schmid
"Hamming Embedding and Weak geometry consistency for large scale image search"
Proceedings of the 10th European conference on Computer vision, October, 2008 

To reach us:

matthijs.douze@inria.fr
herve.jegou@inria.fr

Legal
=====

Copyright INRIA 2008
Licence: GPL
Written by Matthijs Douze
