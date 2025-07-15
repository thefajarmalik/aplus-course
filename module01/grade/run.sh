#!/bin/bash

pip3 install requests cryptography

DEBUG=true

#GRADER_LOG="/feedback/grading-script-errors"
STUDENT_LOG="/feedback/out"

mkdir /exercise-run/
cp -R /exercise/* /exercise-run/
cp -R /submission/user/* /exercise-run/

cd /exercise-run/ || exit

output="$(python3 collect_grade.py)"

echo "${output}" >"${STUDENT_LOG}"

grade

exit 0
