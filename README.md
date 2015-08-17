# MelbDjango School Lesson Five

### Assignment 1

**Important:** Check out our first assignment here: https://github.com/melbdjango/melbdjango-assignment

---


Congratulations, you've made it to the git repository for our fifth lesson. Hopefully you also made it to the class and some of this makes sense to you.

Check our RESOURCES.md for some links we think you'll find handy.


## Homework Checklist

- [ ] [Fork this repository][gh-fork]
- [ ] Clone the repo to your own machine
- [ ] Use the virtualenv you created in previous lesson
- [ ] Convert time-tracker forms and views to ModelForms and Generic Class Based Views
- [ ] Bonus 1: Create a RedirectView to redirect visitors from the root of the site (/) to the /clients/ page
- [ ] Bonus 2: Add a button to the "entries" form (/entries/) called "Create Entry with End Now"
  - This button should be an alternative submit button that automatically sets the end time to be the current time

When you've completed some or all of the homework please make a [Pull Request][gh-pr] against this repository. If you submit your work before Wednesday evening we'll give you feedback before the next class.

If you'd like help, make a Pull Request with your incomplete work and ask a question to @darrenfrenkel, @sesh or @funkybob.


## Displaying the class slides

Install reveal-md with npm and use that to display the class slides.

```
    npm install -g reveal-md
```

From within the `lesson-five` repo:

```
    cd slides
    reveal-md CLASS.md --theme melbdjango
```

[gh-fork]: https://help.github.com/articles/fork-a-repo/
[gh-pr]: https://help.github.com/articles/using-pull-requests/
[dj-request-response]: https://docs.djangoproject.com/en/1.8/ref/request-response/
[mdn-html]: https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Introduction
