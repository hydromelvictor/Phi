**PHI - ALX WEBSTACK PROJECT - BACKEND SOFTWARE ENGINEER SPECIALIZATION END**
==============================================================================

![Phi](./phi/static/svg/phi-320.svg)

Phi is a web application designed for professionals of all backgrounds and disciplines to share their passion for work, promote their sector of activity and find new career or even a new job. Phi is also a place to spend a weekend with colleagues and friends through private and group discussions.

this adventure to Phi is a composition of three backend engineers:

| full names | github link | linkedin link | twitter link | stackoverflow link |
| :---------:| :----------:| :------------:| :-----------:| :-----------------:|
| Hydromel Victor Doledji | [*harkinder-dark*](https://github.com/harkinder-dark) | [*hydromel*](https://www.linkedin.com/in/hydromel/) | [*WarningCode*r](https://twitter.com/WarningCode) | [*hydromel*](https://stackoverflow.com/users/20591064/hydromel) |
| Caren Kathambi | [*CaraNerac*](https://github.com/CaraNerac) | [*Cara Nerac*](linkedin) | [*Twitter*]() | [*StackOverflow*]() |
| Timo kamau | [*github*]() | [*linkedIn*]() | [*Twitter*]() | [*StackOverflow*]() |
<br>

## ![Phi](./phi/static/svg/phi-32.svg)[**visit our site**]()

## Architecture

* [**Phi - project root**](.)
  * [**phi - project**](../Phi)
    * [**db - all database in mongodb**](./phi/db/)
      * [****init**.py - database create and init**](./phi/db/__init__.py)
      * [**chats.py - chat collections**](./phi/db/)
      * [**comments.py - comments collections**](./phi/db/comments.py)
      * [**friends.py - friends request collections**](./phi/db/friends.py)
      * [**posts.py - posts collection**](./phi/db/posts.py)
      * [**settings.py - users configurations collections**](./phi/db/settings.py)
      * [**users.py - users collections**](./phi/db/users.py)
    * [**media - users upload files**](./phi/medias/)
      * [**...**](media)
    * [**static**](./phi/static)
      * [**css-js-img-font-svg...**](css-js-img-font-svg)
    * [**templates**](./phi/templates)
      * [**html**](...)
    * [****init**.py - project init**](./phi/__init__.py)
    * [**auth - authentication file**](./phi/auth.py)
    * [**chat - chat files**](./phi/chat.py)
    * [**const - constant file**](./phi/const.py)
    * [**news - news file**](./phi/news.py)
    * [**profil - profil configure file**](./phi/profil.py)
  * [**root - sensitive file**](../Phi/root/)
    * [**__init__.py**](../Phi/root/__init__.py)
    * [**.env - hidden file because contains the configuration for the server**](../Phi/root/..)
    * [**jinja.py - custom test and filter for jinja templates**](../Phi/root/jinja.py)
  * [**README.md - this file**](README.md)
  * [**requirement.txt - all modules and frameworks use file**](requirement.txt)
  * [**wsgi.py - run file**](wsgi.py)

## **rum project**

```
myterminal:$ git clone https://github.com/harkinder-dark/Phi.git
myterminal:$ cd Phi
```

**linux**
--------------------------------------------------------

```
myterminal:$ python3 -r requirement.txt

# launch
myterminal:$ python3 wsgi
```

**windows**
--------------------------------------------------------

```
python -r requirement.txt

# launch
myterminal:$ python -m wsgi
```

<br>

## Sign Up and Login

| Sign Up | Login |
|:-------:|:-----:|
| ![](./phi/static/img/Capture.PNG) | ![](./phi/static/img/Capture1.PNG) |

<br>

## Composition of the project

* <span style="color: deepskyblue; font-weight: bolder;">Authentication</span>
  * user registration and authentication required before access
* <span style="color: deepskyblue; font-weight: bolder;">news</span>
  * a set of user posts constituting news that can be consulted immediately after authentication
* <span style="color: deepskyblue; font-weight: bolder;">profile management</span>
  * access to your private user profile allowing the modification of the user name, the profile photo, and also the entry of more personal information allowing your profile to be more reinforced and admirable for public consultation which increases the possibility of friendship and much more...
  access to the parameter allowing you to control who could see your public profile, comment on your posts, write to you, send you friend requests and much more.
  you have access to the modification of your password and of course to the deletion of your account which leads to the total, immediate, definitive and irrecoverable deletion of your data and of course all this in one place and tidy
* <span style="color: deepskyblue; font-weight: bolder;">write posts</span>
  * at your disposal a complete tool for writing your posts capable of integrating text, images, links, videos and much more
* access to the public profile of all users
  * yes access to the public profile of course if the user's configuration allows you
* <span style="color: deepskyblue; font-weight: bolder;">I let you make the other discoveries on your own ...</span>
