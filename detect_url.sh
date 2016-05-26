#!/bin/bash

res=`ps -ef | grep "firefox" | wc -l`
echo $res
if test $res -lt 3
then
	date '+%b %e %T %Y' >>/home/zcq/PycharmProjects/PyTest/urllog.txt
	python /home/zcq/PycharmProjects/PyTest/downloadurl.py >>/home/zcq/PycharmProjects/PyTest/urllog.txt

fi

