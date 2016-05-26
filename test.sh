#!/bin/bash

res=`ps -ef | grep "firefox" | wc -l`
echo $res
if test $res -le 3
then
	date '+%b %e %T %Y' >>/home/zcq/PycharmProjects/PyTest/test.txt
	python /home/zcq/PycharmProjects/PyTest/111.py >>/home/zcq/PycharmProjects/PyTest/test.txt
fi