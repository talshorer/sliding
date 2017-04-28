#! /bin/bash
ret=0
for f in $(find . -name "*.py"); do
	echo -n "$f "
	wc -l < $f
	$PYTHON -m pep8 -r $f || ret=1
	$PYTHON -m pyflakes $f || ret=1
done
exit $ret
