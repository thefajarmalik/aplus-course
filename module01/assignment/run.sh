#!/bin/bash

pip3 install requests cryptography python-dateutil

DEBUG=true

#GRADER_LOG="/feedback/grading-script-errors"
STUDENT_LOG="/feedback/out"

mkdir /exercise-run/
cp -R /exercise/* /exercise-run/
cp -R /submission/user/* /exercise-run/

cd /exercise-run/ || exit

output="$(python3 create_login_url.py)"

echo "${output}" >"${STUDENT_LOG}"

grade 0

exit 0
