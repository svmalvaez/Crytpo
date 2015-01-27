$(function(){

	function sendForm(btn, form){
		var loader = btn.children('.loader');
		var btn_txt = btn.children('.txt');
		var btn_txt_cpy = btn_txt.text();

		$.ajaxPrefilter(function( options, _, jqXHR ) {
            if ( options.onreadystatechange ) {
                var xhrFactory = options.xhr;
                options.xhr = function() {
                    var xhr = xhrFactory.apply( this, arguments );
                    function handler() {
                        options.onreadystatechange( xhr, jqXHR );
                    }
                    if ( xhr.addEventListener ) {
                        xhr.addEventListener( "readystatechange", handler, false );
                    } else {
                        setTimeout( function() {
                            var internal = xhr.onreadystatechange;
                            if ( internal ) {
                                xhr.onreadystatechange = function() {
                                    handler();
                                    internal.apply( this, arguments ); 
                                };
                            }
                        }, 0 );
                    }
                    return xhr;
                };
            }
        });
	
		var chunked_response = function(data){
			res = (data).split('JSON!_!SEP')
    		l_d = res.length
    		res = res[l_d-1]
    		try{
    			res = JSON.parse(res)
    		}catch(e){
    			console.error('Could not parse json response')
    		}
    		return res
		}

		var xhr = $.ajax({
			beforeSend: function(){
				$('.opmodes-sub').prop('disabled', true)
				btn_txt.text('-')
				loader.spin({
					lines: 8,
					radius: 0,
					width: 4
				})
			},
			url: btn.data('action'),
			type: 'POST',
			data: new FormData(form),
	        cache: false,
	        contentType: false,
	        processData: false,
	        onreadystatechange: function(xhr){
	        	if(xhr.readyState === 3){
	        		data = chunked_response(xhr.responseText);
		        	$('.response_status').text(data.status_txt)
		        }
	        },
			success: function(res){
				res = chunked_response(res);
				$('.response_status').text(data.status_txt)

				if(res.zip_id){
					iframe = $('#download_iframe')[0]
					var _type = btn.data('type');

					if(_type === 'decrypt')
						iframe.src = '/modes-of-operation/get_img/'+res.zip_id+'/'
					else
						iframe.src = '/modes-of-operation/get_zip/'+res.zip_id+'/'

				}
			},
			error: function(errs){
				console.log('Error en comunicación con el servidor');
			},
			complete: function(jqxhr, txt){
				loader.text('');
				btn_txt.text(btn_txt_cpy)
				$('.opmodes-sub').prop('disabled', false)

				$('.img-sd').text('No se ha selecc...')
				form.reset()
			}
		})

	}

	$('.opmodes-sub').on('click', function(e){
		e.preventDefault();
		var $elf = $(this);
		var _type = $elf.data('type');
		var form  = $('#opmodes-form');
		if( _type === 'decrypt'){
			var opmode = prompt('Set operation mode to decrypt. \n Options are: ECB,CBC,CFB,OFB, CTR: ');
			if (opmode === null){
				alert('Operation mode not supported ;)');
				return false;
			}

			$('input[name=decryption_mode]').val(opmode)
			sendForm($elf, form[0])
		}else{
			//form.attr('action', $elf.data('action'))
			//form.submit()
			sendForm($elf, form[0])
		}

	})

	$('.file_cvr').on('click', function(e){
		console.log("Entro a file")
		e.preventDefault();
		var $elf = $(this);
		var file_input = $($elf.data('input'))

		file_input.click()
		file_input.on('change', function(){
			$('.img-sd').text('Archivo: '+$(this).val().replace('C:\\fakepath','.../'))
		})
	})
})