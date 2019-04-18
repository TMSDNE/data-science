create table if not exists Summary(
  id integer primary key,
  Date varchar(10),
  Commentary varchar(3000)
); 

create table if not exists Plotly(
  id integer primary key,
  Date varchar(10),
  Link varchar(255)
);
