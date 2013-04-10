function recalc_sum(event) {
	var tableElem = document.getElementById('items');
	if (!tableElem)
		return

	var counts = tableElem.getElementsByTagName('input');

	var summa = 0;  // ДОСТАВКА!!

	for (var i=0; i<counts.length; i++) {
		var input = counts[i];
		if 	(input.name.indexOf('count_') == 0){
			var cod = input.name.substr(6, 20);
			var p = document.getElementById('price_' + cod);
			if (p){
				cnt = parseInt(input.value);
				pr = parseFloat(p.innerHTML);
				summa = summa + pr * cnt;
			}
			var sum = document.getElementById('summa');
			sum.innerHTML = Math.round(summa);
		}
	}
}
//------------------------------------------------------------------------
function add_product(event) {
        event = event || window.event;
        var clickedElem = event.target || event.srcElement;
        var r =  clickedElem.id.match('_([0-9]+)');
		if (!r)
			return // ничего не выбрали
		id = r[1]
		s ="cnt_"+id;
		input_cnt = document.getElementById(s);
		if (!input_cnt)
			return
		// Проверяем что там натуральное число не больше 9999
		if ( !input_cnt.value.match('^[1-9][0-9]{0,3}$') )
		{
			alert('Укажите количество товара.')
			return
		}
		var c = $.cookie('basket')

		if (!c || c.search( '(^|\.)(' + id + '-[0-9]+)(\.|$)' ) < 0 ){
			if (c)
				c = c + '.' + id + '-' + input_cnt.value
		 	else c = id + '-' + input_cnt.value
			$.cookie('basket', c,  {path: '/' })

			cnt = 1
			for (i = 0; i < c.length; i++){
				if (c[i] == '.') cnt++
			}
		 } else{
				ar = c.split('.')
				for (i = 0; i < ar.length; i++){
					if (ar[i].search('^' + id + '-') == 0) {
						ar[i] = id + '-' + input_cnt.value;
						break;
					}
				}
				c = ar.join('.')
				$.cookie('basket', c,  {path: '/' })
		 }
		}

//------------------------------------------------------------------------
function show_msg(msg){
		// показать уведомлялку
		$('.bottom-right').notify({
		    message: { text: msg },
		    type: 'alert alert-info'
		  }).show();
}

//------------------------------------------------------------------------
function clear_basket(){
		$.cookie('basket', '',  {path: '/' })
	}

//------------------------------------------------------------------------
function basket_get_count(id){
	var c = $.cookie('basket')
	if (!c) return 0
	
	ar = c.split('.')
	for (i = 0; i < ar.length; i++){
		if (ar[i].search('^' + id + '-') == 0) {
			cnt = ar[i].substring(ar[i].search('-') + 1)
			return cnt
			}
		}
	}
	
//------------------------------------------------------------------------
function delete_item(event){
	event = event || window.event;
	var clickedElem = event.target  || event.srcElement;
	var r = clickedElem.id.match('del_([0-9]+)');
	if (!r)
			return // ничего не выбрали
	var c = $.cookie('basket');
	id = r[1];
	if (c)
		ar = c.split('.')
		for (i = 0; i < ar.length; i++){
			if (ar[i].search('^' + id + '-') == 0) {
				ar.splice(i, 1)
				break;
			}
		}		
		c = ar.join('.')
		$.cookie('basket', c,  {path: '/' })
	}

//////////////////////////////////////////////////////////////////////////////////
	
	// сохраняем состояние дерева
	function save_tree(){
		var s=''
		$('i').each(function(index){
		if 	($(this).hasClass('icon-minus'))
			s += $(this).attr('data-target').replace('#node_', '') + '#'
		});
		$.cookie('node_opened', s,  {path: '/' });
	}

	function show_node(s){
		if (s.length > 1) {
			ar = $('.treelist').find('i');
			jQuery.each(ar, function(i, e){
				var id = '#' + $(e).attr('data-target').replace('#node_', '') + '#';
				if (s.search(id) != -1){
					$(e).removeClass('icon-plus');
					$(e).addClass('icon-minus');
					$($(e).attr('data-target')).addClass('in');
				}
			})
			save_tree();
		}
	}

	function show_active_node(s){
		if (s.length > 1) {
			ar = $('.treelist').find('a');
			jQuery.each(ar, function(i, e){
				var id = '#' + $(e).attr('href').replace('/category/', '') + '#';
				if (s.search(id) != -1){
					$(e).addClass('active-node');
				}
			})
		}
	}

   // Обработка раскрытия узлов дерева
	function toggleTreeListNode (e) {
		var elem = $(e.target.parentNode).children('i');
		if (!elem) return;
		elem.toggleClass('icon-plus');
		elem.toggleClass('icon-minus');
		save_tree();
	}




