from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Optional, Length


class CreateItem(FlaskForm):
    id = StringField("Item ID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired(), Length(max=60, message="Name is too long")])
    description = TextAreaField("Description", validators=[Optional(), Length(max=256, message="Too long")])
    price = FloatField("Price", validators=[DataRequired()])
    stock = IntegerField("Stock", validators=[DataRequired()])
    submit = SubmitField("Create Item")


class UpdateItem(FlaskForm):
    pass


class BuyItem(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Buy", validators=[DataRequired()])
