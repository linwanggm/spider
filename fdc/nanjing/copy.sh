path=`pwd`"/data/"`date +%Y`
psql -c "copy nanjing_current_data from '$path/current_time.txt' delimiter ','"
psql -c "copy nanjing_month_statistics_town_num from '$path/month_statistics_town_num.txt' delimiter ','"
psql -c "copy nanjing_month_statistics_town_price_rate from '$path/month_statistics_town_price_rate.txt' delimiter ','"
psql -c "copy nanjing_month_statistics_town_size_rate from '$path/month_statistics_town_size_rate.txt' delimiter ','"
