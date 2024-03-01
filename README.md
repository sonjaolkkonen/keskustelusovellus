# Keskustelusovellus

Sovellus on kiipeilyyn keskittyvä keskusteluforum, joka sisältää kiipeilyn eri osa-alueisiin liittyviä keskustelualueita. Jokainen keskustelualue keskittyy tiettyyn aiheeseen, ja ne muodostuvat viestejä sisältävistä keskusteluketjuista. Sovelluksella on kahdenlaisia käyttäjiä, peruskäyttäjiä ja ylläpitäjiä. 

## Sovelluksen ominaisuudet

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan viestiketjuista ja mihin keskustelualueeseen mikin ketju kuuluu sekä viestiketjun aloitusajankohdan, vastauksien määrän ja viimeksi lähetetyn vastauksen ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden viestissä tai otsikossa on annettu sana.
- Käyttäjä voi antaa kullekin viestille yhden äänen ja annettujen äänien määrä näkyy kunkin viestin kohdalla.
- Ylläpitäjä voi lisätä keskustelualueita.
- Ylläpitäjä voi poistaa myös muiden lähettämiä ketjuja ja viestejä.

## Käynnistysohjeet

1) Kloonaa repositio omalle koneellesi:
   ```
   git clone git@github.com:sonjaolkkonen/keskustelusovellus.git
2) Luo juurikansioon .env-tiedosto ja tallenna sinne seuraava sisältö:
   ```
   DATABASE_URL=<tietokannan-paikallinen-osoite>
   SECRET_KEY=<salainen-avain>
3) Luo Pythonin virtuaaliympäristö projektikansioon:
   ```
   python3 -m venv venv
4) Käynnistä virtuaaliympäristö:
   ```
   source venv/bin/activate
5) Asenna sovelluksen riippuvuudet:
   ```
   pip install -r requirements.txt
6) Määritä tietokannan skeema komennolla:
   ```
   psql < schema.sql
7) Käynnistä sovellus virtuaaliympäristössä:
   ```
   flask run 
