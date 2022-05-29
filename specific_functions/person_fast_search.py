

def search(dbs, criterias):
    """
    dbs: databse connection
    return searched licenses
    activity_id and season_id for referee search
    """

    sql = '''
select p.person_id,
case 
    when p.rfen_id != 0 then (p.rfen_id || '. ' || p.surname  || ', ' || p.name)
    else (p.person_id || '. ' || p.surname  || ', ' || p.name)
end
from persons as p where
{}
{} like {}
order by p.surname, p.name '''
    sql = sql.format(
        dbs.normalize("p.person_id||' ' ||p.surname||' ' ||p.name||' ' ||p.lev_id||' ' ||p.rfen_id"),
        dbs.normalize("?"))

    values = (('%{}%'.format(
        '%'.join([i for i in criterias.split(' ') if i])), ), )
    coincidences = dbs.exec_sql(sql=sql, values=values)

    return coincidences
