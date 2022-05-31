import pytest
from scrapy.http import HtmlResponse

from scraping.spiders.poland_rjps import QuotesSpider


@pytest.fixture
def normal_place():
    raw_text = """
    



<div class="zamknij" title="Zamknij">
	<button aria-label="zamknij" type="button" class="btn p-0" onclick="mapa.zamknijListe();">
		<em class="fa fa-lg fa-times"></em>
	</button>
</div>
<hr/>

<div class="lista-jednostek">
	
	
		
		





<div class="row jednostka" data-id="3499" data-typ-id="5">
    
    
    <div class="data-aktualizacji-mobile text-right w-100">
        	data aktualizacji:  2018-02-05
    </div>
    <div class="col-12 col-lg-7 pl-0">
        <div class="row">
            <div class="col-11">
                <h3 class="nazwa" title="Nazwa jednostki">
                    <a class="jednostka-pelna-nazwa" href="#" onclick="przegladarka.pokazKarta(3499,5); return false;">
                        Miejski Ośrodek Pomocy Społecznej w Zabłudowie
                    </a>
                </h3>
            </div>
            <div class="ulubiona-jednostka"></div>
        </div>
        <div class="row mb-2">
            <div class="col-12" title="Typ jednostki">
                <span>Ośrodek pomocy społecznej</span>
            </div>
        </div>
        <div class="row">
            <div class="col-12 col-sm-6">
               <div class="adresdiv" >
<div class="flex flex-row" title="Adres">
<div class="dane-icon">
<span class="fa-stack fa-2x"> <em
 class="fa fa-square-o fa-stack-2x"></em> 
<em class="fa fa-map-marker fa-stack-1x"></em>
</span>
</div>
<div class="flex flex-column justify-content-center">
<span>16-060 Zabłudów</span>
<span> ul. Rynek 8</span>
</div>
</div>
</a>
</div>

            </div>
            
                <div class="col-12 col-sm-6">
                    <div class="adresdiv" >
<a aria-label="e-mail" href="mailto:biuro@mops-zabludow.pl">
<div class="flex flex-row" title="Email">
<div class="dane-icon">
<span class="fa-stack fa-2x"> <em
 class="fa fa-square-o fa-stack-2x"></em> 
<em class="fa fa-envelope-o fa-stack-1x"></em>
</span>
</div>
<div class="flex flex-column justify-content-center">
<div class=" underlineLink wrap-anywhere adreslink">biuro@mops-zabludow.pl</div>
</div>
</div>
</a>
</div>

  	            </div>
            
			
				<div class="col-12 col-sm-6">
					<div class="adresdiv" >
<a aria-label="numer telefonu" href="tel:85 7188100">
<div class="flex flex-row" title="Telefon">
<div class="dane-icon">
<span class="fa-stack fa-2x"> <em
 class="fa fa-square-o fa-stack-2x"></em> 
<em class="fa fa-phone fa-stack-1x"></em>
</span>
</div>
<div class="flex flex-column justify-content-center">
<span class="wrap-anywhere">tel. 85 7188100</span>
</div>
</div>
</a>
</div>

				</div>
			
		    
				<div class="col-12 col-sm-6">
                    <div class="adresdiv" >
<a aria-label="strona internetowa" href="http://bip.mops.um.zabludow.wrotapodlasia.pl" target="_blank">
<div class="flex flex-row" title="Strona www">
<div class="dane-icon">
<span class="fa-stack fa-2x"> <em
 class="fa fa-square-o fa-stack-2x"></em> 
<em class="fa fa-globe fa-stack-1x"></em>
</span>
</div>
<div class="flex flex-column justify-content-center">
<div class=" underlineLink wrap-anywhere adreslink" target="_blank">http://bip.mops.um.zabludow.wrotapodlasia.pl</div>
</div>
</div>
</a>
</div>

	            </div>
            
	    	
				<div class="col-12 col-sm-6">
						
						
							<div class="adresdiv" >
<a aria-label="Wnioski o świadczenie" href="//" target="_blank">
<div class="flex flex-row" title="Wnioskuj o świadczenie - platforma Emp@tia">
<div class="dane-icon">
<span class="fa-stack fa-2x"> <em
 class="fa fa-square-o fa-stack-2x"></em> 
<em class="fa fa-file-text-o fa-stack-1x"></em>
</span>
</div>
<div class="flex flex-column justify-content-center">
<span class="wrap-anywhere">Wnioskuj o świadczenie - platforma Emp@tia</span>
</div>
</div>
</a>
</div>

						
						
				</div>
    		
    </div>
    </div>
    <div class="col-12 col-lg-5 px-0">
        <div class="data-aktualizacji text-right w-100">
        	data aktualizacji:  2018-02-05
        </div>
        <div class="zdjecie">
            <div title="Brak zdjęcia">
                <div class="row justify-content-center">
                    <div class="col text-center pt-3">Brak zdjęcia</div>
                </div>
                <div class="row justify-content-center">
                    <div class="col text-center pt-4 pb-5">
                    	<span class="fa-stack fa-lg">
                    		<i class="fa fa-camera fa-stack-1x"></i>
                    		<i class="fa fa-ban fa-stack-2x text-danger"></i>
                    	</span>
                    </div>
                </div>
            </div>
            <a aria-label="Pokaż kartę dla jednostki" onClick="przegladarka.pokazKarta(3499,5)">
                <img alt="Symbol brakującego zdjęcia - jednostka nie dodała żadnej fotografii"/>
            </a>
        </div>
    </div>
    <div class="col-12 pt-2" title="Szczegóły">
        <button class="btn btn-wj btn-wj-blue" onclick="przegladarka.pokazKarta(3499,5)">
            Szczegóły
        </button>
    </div>
</div>
<hr/>
<script>
    lista.initJednostka($('#mapaContainer'), 3499);
</script>

	
</div>
    """
    # TODO: move raw text into file
    return HtmlResponse(body=raw_text, encoding='utf-8', url='test.com')


class TestQuotesSpider:
    def test_parse_name(self, normal_place):
        name = QuotesSpider().parse(normal_place, category='test').get('name')
        assert name == 'Miejski Ośrodek Pomocy Społecznej w Zabłudowie'

    def test_parse_address(self, normal_place):
        address = QuotesSpider().parse(normal_place, category='test').get('address')

        assert address == '16-060 Zabłudów ul. Rynek 8'

    def test_parse_email(self, normal_place):
        description = QuotesSpider().parse(normal_place, category='test').get('description')
        assert 'biuro@mops-zabludow.pl' in description

    def test_parse_phone(self, normal_place):
        description = QuotesSpider().parse(normal_place, category='test').get('description')
        assert 'tel. 85 7188100' in description

    def test_parse_website(self, normal_place):
        description = QuotesSpider().parse(normal_place, category='test').get('description')
        assert 'http://bip.mops.um.zabludow.wrotapodlasia.pl' in description

    def test_parse_update_date(self, normal_place):
        description = QuotesSpider().parse(normal_place, category='test').get('description')
        assert 'data aktualizacji:  2018-02-05' in description

