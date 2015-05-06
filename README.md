## intervention

`intervention` is a work in progress for disabling input to my computer,
showing me the current time, and making me ask myself if I'm being intentional.

~~It requires `sudo` NOPASSWD access on OS X to filter keyboard input. Wrapping
it in an application might allow it to be used with the OS X Accessibility API
instead.~~

### Installation

```sh
$ pip3 install intervention
$ crontab -e
*/15 * * * * /usr/local/bin/intervention  # add this line
```

It looks like this:

![screenshot](https://i.imgur.com/mIRAUTr.png)
