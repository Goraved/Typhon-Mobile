#!/bin/bash
if [[ ! -f requirements.txt ]]; then
    cd ..
fi
#docker build -t
source venv/bin/activate
_now=$(date +%Y-%m-%d_%H:%M:%S)
dir=$(pwd)

killall -KILL node

# Path to base folder of tests
PYTHONPATH="${PYTHONPATH}:${dir}"
export PYTHONPATH

## Set environment

export ENVIRONMENT=${ENVIRONMENT:=stg}
export RUN_TESTS=${RUN_TESTS:=mobile/suite}
export DEVICE=${DEVICE:=iphone_7}  # test_emu; br_pixel; br_iphone_8
export PLATFORM=${PLATFORM:=ios}
export APP_URL
export REMOTE_SETTINGS_PASS
export ANDROID_PACKAGE
export BUILD_TYPE${BUILD_TYPE:=release}
echo "Test run folder - $RUN_TESTS"
echo "Environment - $ENVIRONMENT"
echo "Device - $DEVICE"
echo "Platform - $PLATFORM"
echo "Configuring $PLATFORM"
echo "App build type = $BUILD_TYPE"
export APP_URL
echo "Browserstack app url - $APP_URL"

if [[ -z "$APP_URL" ]]; then
printf '\nWRONG!\n\nNo app url!\n'
exit 1
fi

cd ${dir}
pip install -r requirements.txt --quiet
mkdir -p allure-results
mkdir -p allure-results/archive
mkdir -p allure-results/history

# Remove temp test data
rm -rf temp_files || echo ""

# Run The tests in project folder
echo "Running tests"
# Regular run
py.test ${dir}/tests/${RUN_TESTS} --alluredir ${dir}/allure-results/archive/${_now}
echo "Test run finished"

## Environments settings
cp ${dir}/allure-results/environment.properties ${dir}/allure-results/archive/${_now}

## Copy previous history
mkdir ${dir}/allure-results/archive/${_now}/history
cp ${dir}/allure-results/history/*.json ${dir}/allure-results/archive/${_now}/history

## Generate allure report folder
allure generate ${dir}/allure-results/archive/${_now} -o ${dir}/allure-results/archive/${_now}/generated-report

## Saving current test run to history
rm ${dir}/allure-results/history/*
cp -r ${dir}/allure-results/archive/${_now}/generated-report/history/*.json ${dir}/allure-results/history
find . | grep -E "(__pycache__|\.pyc|\.pyo$|.pytest_cache)" | xargs rm -rf

## Open generated report
allure open ${dir}/allure-results/archive/${_now}/generated-report
