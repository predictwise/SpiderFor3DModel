#!/bin/bash

res=`ps -ef | grep "firefox" | wc -l`
echo $res
if test $res -lt 3
then
	date '+%b %e %T %Y' >>/home/zcq/PycharmProjects/PyTest/kmzlog.txt
	python /home/zcq/PycharmProjects/PyTest/downloadall.py >>/home/zcq/PycharmProjects/PyTest/kmzlog.txt
fi

