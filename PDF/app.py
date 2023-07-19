from flask import Flask, render_template, request, make_response
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        location = form.location.data
        pdf_data = generate_pdf(name, location)
        response = make_response(pdf_data)
        response.headers['Content-Disposition'] = 'attachment; filename=userdata.pdf'
        response.headers['Content-Type'] = 'application/pdf'
        return response
    return render_template('index.html', form=form)

def generate_pdf(name, location):
    pdf_buffer = io.BytesIO()
    p = canvas.Canvas(pdf_buffer)

    p.setFont("Helvetica", 12)
    p.drawString(100, 750, "Name: {}".format(name))
    p.drawString(100, 700, "Location: {}".format(location))

    p.showPage()
    p.save()

    pdf_data = pdf_buffer.getvalue()
    pdf_buffer.close()
    return pdf_data

if __name__ == '__main__':
    app.run(debug=True)
    app.run(port=5000)