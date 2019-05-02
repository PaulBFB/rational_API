drop table process;

create TABLE process (
    batch_id integer primary key,
    created datetime,
    app_version character(14),
    care_recipe boolean,
    category int,
    chamber_id int,
    device_family character(3),
    device_name varchar(16),
    device_serialnumber varchar(32),
    finished boolean,
    group_id int,
    group_name varchar(16),
    process_id int,
    recipe_id int,
    recipe_name varchar(64),
    start datetime,
    temp_unit varchar(8)
);
