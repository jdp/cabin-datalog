#!/bin/bash
grep -E '^(import|from)' *.py | perl -lne '
BEGIN {print "digraph {"}
/^([a-z]+)\.py:from ([a-z_]+)/ && {print $1, " -> ", $2, ";"}; 
/^([a-z]+)\.py:import ([a-z_]+)/ && {print $1, " -> ", $2, ";"};
END {print "}"}
'
