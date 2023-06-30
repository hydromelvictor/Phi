class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])

    # add a hidden field for content to receive from Quill
    content = HiddenField(
        'content',
        validators=[Length(0, 25500), DataRequired()],
    )

    submit = SubmitField('Create Post')


create_post.html:

<!-- create the hidden text field -->
{{ form.hidden_tag() }}

<!-- script for Quill editor -->

<script>
  // When the submit button is pressed, retrieve several pieces of info
  // from the QuillJS API (https://quilljs.com/docs/api/#content), copy
  // them into to WTForms hidden fields, and submit the form
  var submit_entry = function () {

    // Get the contents of the text editor
    var hidden_text_field = document.getElementById('content');
    // hidden_text_field.value = JSON.stringify(quill.getContents());
    hidden_text_field.value = quill.root.innerHTML;
  }

  // Attach the onclick function to the submit button Flask-WTF creates
  var new_post_form = document.getElementsByClassName('form')[0];

  new_post_form.onsubmit = submit_entry;
</script>






def save_picture(pic):
    """Save blog picture."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/blog_pics', pic_fn)

    pic.save(pic_path)

    return pic_fn


@posts.route('/blog-pic-uploader', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':

        f = request.files['image']

        new_file_name = save_picture(f)
        return '/static/blog_pics/' + new_file_name





