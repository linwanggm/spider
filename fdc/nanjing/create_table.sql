--nanjing fangdichan data
--current data
CREATE TABLE nanjing_current_data(city name, time date, rengou int, chengjiao int, xinfangshangshi int);
--new house last month
CREATE TABLE nanjing_month_statistics_town_num(city name, time date, town name, zhuzhai_num int, zhuzhai_area int, office_unit int, office_area int, business_unit int, business_area int);
-- monthstatistics town size rate
CREATE TABLE nanjing_month_statistics_town_size_rate(city name, time date, area_region name, num int, area int, rate float);
--month statistics town price rate
CREATE TABLE nanjing_month_statistics_town_price_rate(city name, time date, price name, num int, area int, rate float);

