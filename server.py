# App config.
from flask import *
from wtforms import *
from Orienteerumiseks import *

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        si = request.args.get('si')
        form = ReusableForm(request.form)


        if request.method == 'POST':
            is_eol = False
            is_nimi = False

            name = request.form
            if name['EOL kood'] != "":
                eol = name['EOL kood']
                is_eol = True
            elif name["Nimi"] != "":
                nimi = name["Nimi"].strip().capitalize()
                is_nimi = True
            else: print("Puudub")

            if name["si_pulk"] == "":
                kas_oma_si = True
            else:
                kas_oma_si = False

            if is_nimi:
                teine = nimega(nimi)
                try:
                    teine.reset_index(inplace=True)
                    if teine.iloc[0].array[0] == teine.iloc[1].array[0]:
                        teine = teine.iloc[0]
                        teine = teine.to_frame().transpose()
                    teine.set_index("Kood", inplace=True)
                except: teine.set_index("Kood",inplace = True)
                pikkus = teine.shape[0]
                if not teine.empty:
                    if pikkus > 1:

                        flash(Markup(teine.to_html()))
                        return redirect(url_for('topelt_eol',si= name["si_pulk"],nimi=nimi))
                    if pikkus == 1:
                        for eol, others in teine.iterrows():
                            if kas_oma_si:
                                si = otsi_si(int(eol))
                            else:
                                si = name["si_pulk"]
                            return redirect(url_for('vastus',si=si,eol=eol))
                else: return redirect(url_for('uus_eol',nimi = nimi,si=name["si_pulk"]))
            elif is_eol:
                if kas_oma_si:
                    si = otsi_si(int(eol))
                else:
                    si = int(name["si_pulk"])
                return redirect(url_for('vastus', si=si, eol=eol))





        return render_template('regamine.html', form=form)



    @app.route("/uus_eol", methods=['GET', 'POST']) #return redirect(url_for('uus_eol',nimi = nimi,si=si))
    def uus_eol():
        form = ReusableForm(request.form)
        nimi = request.args.get('nimi')
        si = request.args.get('si')
        eol = -1
        if request.method == 'POST':
            name = request.form
            if name["Elukoht"] != "":
                aasta = uusEOL(nimi,name["sunniaeg"],name["sugu"],name["Elukoht"],name["Klubi"],name["Email"])
                return redirect(url_for('vastus', si=si, eol=eol,nimi=nimi, sunniaeg=aasta))
            else:
                return redirect(url_for('vanus', si=si, eol=eol,nimi=nimi))
        return render_template('uus_eol.html', form=form)

    @app.route("/topelt_eol", methods=['GET', 'POST'])
    def topelt_eol():
        si = request.args.get('si')
        nimi = request.args.get('nimi')
        sunniaeg = request.args.get('sunniaeg')
        if request.method == 'POST':
            eol = request.form
            if eol["EOL kood"] == "":
                return redirect(url_for('uus_eol', nimi=nimi, si=si))
            else:
                return redirect(url_for('vastus', si=si, eol=eol["EOL kood"]))
        return render_template('topelt_eol.html', form=form)



    @app.route("/annavastus", methods=['GET', 'POST'])#return redirect(url_for('vastus',si=si, eol=eol,nimi=nimi))
    def vastus():
        eol = int(request.args.get('eol'))
        si = request.args.get('si')
        nimi = request.args.get('nimi')
        sunniaeg = (request.args.get('sunniaeg'))
        klubi = ''
        if eol < 1:
            eol = 0
        if nimi != None:
            eesnimi, perekonnanimi = nimi.rsplit(" ", 1)

        kas_laps = kasLaps(eol,sunniaeg)



        if eol != 0:
            data = info(eol,si)
            eesnimi = data['Eesnimi']
            perekonnanimi = data['Perekonnanimi']
            klubi = data['Klubi']
            if si == '':
                si = data['Si']
        kas_laps = kasLaps(eol,sunniaeg)

        lng = pd.Series(data={'Eol':eol, 'Si':si, 'Eesnimi':eesnimi, 'Perekonnanimi':perekonnanimi, 'Klubi':klubi, 'Laps/Noor': 'Jah' if kas_laps== 1 else 'Ei' })

        htmlliks = lng.to_frame().transpose().set_index('Eol')

        if request.method == 'POST':
            kinnita = request.form
            return redirect(url_for('saada', si=si, eol=eol,enimi=eesnimi,pnimi=perekonnanimi,sunniaeg=kas_laps))

        flash(Markup(htmlliks.to_html()))
        return render_template('kontroll.html', form=form)




    @app.route("/saada", methods=['GET', 'POST'])
    def saada():
        eol = int(request.args.get('eol'))
        si = request.args.get('si')
        enimi = request.args.get('enimi')
        pnimi = request.args.get('pnimi')
        kas_laps = (request.args.get('sunniaeg'))
        arvuta(eol, si, enimi,pnimi, kas_laps)


        return redirect(url_for('hello'))

    @app.route("/kusivanust", methods=['GET', 'POST'])  # return redirect(url_for('vanus',si=si, eol=eol,nimi=nimi))
    def vanus():
        si = request.args.get('si')
        eol = request.args.get('eol')
        nimi = request.args.get('nimi')
        if request.method == 'POST':
            try:
                kas_noor = request.form['vanus']
                sunniaeg = 2010
            except:
                sunniaeg = 1990
            return redirect(url_for('vastus', si=si, eol=eol,nimi=nimi,sunniaeg=sunniaeg))

        return render_template('vanus.html', form=form)

if __name__ == "__main__":
    app.run()


"""
    @app.route("/si", methods=['GET', 'POST'])
    def si_pulganr():
        form = ReusableForm(request.form)
        if request.method == 'POST':
            si = request.form
            return redirect(url_for('hello',si=si["si_pulk"]))

        return render_template('rendi_si.html', form=form)
"""