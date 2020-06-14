#!/bin/bash

set -x

gcloud_path=$(which gcloud)
script_base_path=/opt/iambot

function prepare_previous () {
  project=$1
  date=$(date +%Y%m%d)
  previous_date=$(date -d '-1 days' +%Y%m%d)
  today_iam=${script_base_path}/${project}_iam_${date}
  previous_day_iam=${script_base_path}/${project}_iam_${previous_date}

  if [[ ! -f "${today_iam}" ]]; then

    ls -d -1 ${script_base_path}/* | grep ${project} | grep -v -e "${previous_day_iam}" -e "_iam$" -e "_iam_newer$" | xargs rm -v

    $gcloud_path projects get-iam-policy ${project} > ${today_iam}

    if [[ ! -f "${previous_day_iam}" ]]; then
      cp ${today_iam} ${previous_day_iam}
    fi

  fi
}

prepare_previous my-project-1
prepare_previous my-project-2

set +x

