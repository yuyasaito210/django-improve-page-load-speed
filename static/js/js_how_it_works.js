$(document).ready(function() {
	$("body").children().each(function() {
		document.body.innerHTML = document.body.innerHTML.replace(/\u2028/g, ' ');
	});
});

function navigate(tab, el) {
	console.log(tab);
	let hide = tab === 'passenger' ? 'owner' : 'passenger';
	$(".tab").removeClass('active');
	$(el).addClass('active');
	$(`.perguntas.${hide}`).addClass('hide');
	$(`.perguntas.${tab}`).removeClass('hide');
}