#!/bin/bash

set -x

python_path=/opt/miniconda/envs/work/bin/python
gcloud_path=$(which gcloud)
script_base_path=/opt/iambot

function check_iam () {
  project=$1
  iam_file=${script_base_path}/${project}_iam
  newer_iam_file=${script_base_path}/${project}_iam_newer

  $gcloud_path projects get-iam-policy ${project} > ${newer_iam_file}
  if [ -f "${iam_file}" ]; then
    ${python_path} ${script_base_path}/check_iams.py \
    ${iam_file} \
    ${newer_iam_file} && \
    cp ${newer_iam_file} ${iam_file}
  else
    cp ${newer_iam_file} ${iam_file}
  fi
}

check_iam my-project-1
check_iam my-project-2

set +x

