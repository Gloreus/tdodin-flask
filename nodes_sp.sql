delimiter $$

CREATE DEFINER=`root`@`localhost` FUNCTION `get_node_by_code`(i_code varchar(32)) RETURNS int(11)
BEGIN
  set @res = null;
	if i_code = '' then
		return @res;
	end if;

	select id  into @res from TreeItem t  where  t.code = i_code;
	if @res is not null then
		return @res;
	end if;

	set @parent_id = null;
	set @i = locate('.', i_code, 1);
	while  @i > 0 do
		set @s = substring(i_code, 1, @i-1) ;

		set @res = null;
		select id  into @res from TreeItem t  where  t.code = @s;
		if @res is null then
				insert into TreeItem (code, parent,  is_node) 
				values        (@s, @parent_id,  1);
				select id  into @res from TreeItem t  where  t.code = @s;
		end if;
		set @parent_id = @res;
		set @i = locate('.', i_code, @i + 1);
	end while;

	insert into TreeItem (code, parent,  is_node) 
		values        (i_code, @parent_id,  1);
	select id  into @res from TreeItem t  where  t.code = i_code;
	
	RETURN @res;
END$$


delimiter $$

CREATE DEFINER=`root`@`localhost` FUNCTION `set_node_by_code`(i_code varchar(32), i_name varchar(255), i_desc text) RETURNS int(11)
BEGIN
		set @node_id  = get_node_by_code(i_code);
		update TreeItem t set
			t.name = i_name,
			t.description = i_desc
		where id = @node_id;
		
RETURN @node_id;
END$$


