path=`pwd`"/data/"`date +%Y`
psql -c "copy beijing_currentdata from '$path/current_time_data.txt' delimiter ','"
