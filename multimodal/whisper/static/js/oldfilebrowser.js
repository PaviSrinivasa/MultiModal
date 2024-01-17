$(document).ready( function() {
	$( '#container' ).html( '<ul class="filetree start"><li class="wait">' + 'Generating Tree...' + '<li></ul>' );
	getfilelist( $('#container') , '/mnt/d/work' );

	function getfilelist( cont, root ) {
		$( cont ).addClass( 'wait' );
		$.post( 'browser.html', { dir: root }, function( data ) {
			$( cont ).find( '.start' ).html( '' );
			$( cont ).removeClass( 'wait' ).append( data );
			if( 'Sample' == root )
				$( cont ).find('UL:hidden').show();
			else
				$( cont ).find('UL:hidden').slideDown({ duration: 500, easing: null });
		});
	}

	$( '#container' ).on('click', 'LI A', function() {
		var entry = $(this).parent();
		if( entry.hasClass('folder') ) {
			if( entry.hasClass('collapsed') ) {
				entry.find('UL').remove();
				getfilelist( entry, escape( $(this).attr('rel') ));
				entry.removeClass('collapsed').addClass('expanded');
			}
			else {
				entry.find('UL').slideUp({ duration: 500, easing: null });
				entry.removeClass('expanded').addClass('collapsed');
			}
		} else {
			$( '#selected_file' ).text( "File:  " + $(this).attr( 'rel' ));
		}
	return false;
	});
});
