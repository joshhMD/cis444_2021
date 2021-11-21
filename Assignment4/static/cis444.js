var jwt = null
function secure_get_with_token(endpoint, data_to_send, on_success_callback, on_fail_callback){
	xhr = new XMLHttpRequest();
	function setHeader(xhr) {
		xhr.setRequestHeader('JWT', data_to_send['jwt']);
	}
	$.ajax({
		url: endpoint,
		data : {'username': data_to_send['username'], 'title': data_to_send['title']},
		type: 'POST',
		datatype: 'json',
		success: function(data)
		{
			return data
		},
		error: on_fail_callback,
		beforeSend: setHeader
	});
}
