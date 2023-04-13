jQuery.fn.stylise = function (options) {

  const flags = {
    isSingleChannel: true,
    resetPeersOnPlay: true
  };

  const settings = jQuery.extend({ mode: 'single-reset' }, options);

  switch (settings.mode) {
    case 'single-reset':
    case 1:
      flags.isSingleChannel = true;
      flags.resetPeersOnPlay = true;
      break;
    case 'single-pause':
    case 2:
      flags.isSingleChannel = true;
      flags.resetPeersOnPlay = false;
      break;
    case 'multi':
    case 3:
      flags.isSingleChannel = false;
      flags.resetPeersOnPlay = false;
      break;
    default:
      console.warn(
        `The stylised mode '${settings.mode}' is not supported.
Please instead choose from
 * single-reset - to have a single active player which resets others when played
 * single-pause - to have a single active player which pauses others when played, or
 * multi - to allow all players to be active simultaneously`);
  }

  var players = [];

  function pad(str, max) {
    str = str.toString();
    return str.length < max ? pad(`0${str}`, max) : str;
  }

  function getProgressReadout(e, d) {
    const se = parseInt(e % 60);
    const me = parseInt((e / 60) % 60);

    const sd = parseInt(d % 60);
    const md = parseInt((d / 60) % 60);

    return `${me}:${pad(se, 2)} of ${md}:${pad(sd, 2)}`;
  }

  function playFromPosition(e, id) {
    const x = e.pageX - jQuery(`#${id} p`).offset().left;

    const player = players.find(e => e.id === id);

    const ew = jQuery(`#${id} p`).width();

    const d = player.controls.duration;

    player.controls.currentTime = d * (x / ew);

    play(id);
  }

  function restart(id) {
    jQuery(`.stylised-play`).show();
    jQuery(`.stylised-pause`).hide();

    const player = players.find(e => e.id === id);
    player.controls.currentTime = 0;
    player.controls.pause();
    jQuery(`#${player.id} .stylised-play`).show();
    jQuery(`#${player.id} .stylised-pause`).hide();
  }

  function pause(id) {

    if (flags.isSingleChannel) {
      jQuery(`.stylised-play`).show();
      jQuery(`.stylised-pause`).hide();
    }

    const player = players.find(e => e.id === id);
    player.controls.pause();
    jQuery(`#${player.id} .stylised-play`).show();
    jQuery(`#${player.id} .stylised-pause`).hide();

  }

  function play(id) {

    for (let i = 0; i < players.length; i++) {
      const player = players[i];
      if (player.id === id) {
        jQuery(`#${player.id} .stylised-pause`).show();
        jQuery(`#${player.id} .stylised-play`).hide();
        player.controls.play();
      } else {
        if (flags.isSingleChannel) {
          jQuery(`#${player.id} .stylised-play`).show();
          jQuery(`#${player.id} .stylised-pause`).hide();
          player.controls.pause();

          if (flags.resetPeersOnPlay) {
            player.controls.currentTime = 0;
          }
        }
      }
    }
  }

  function updateReadout(player) {
    const c = player.controls.currentTime;
    const d = player.controls.duration;
    const r = getProgressReadout(c, d);
    jQuery(`#${player.id} p`).text(r);
    jQuery(`#${player.id} .stylised-time-progress`).width(`${c / d * 100}%`);
    if (c / d === 1) {
      restart(id);
    }
  }

  return this.each(function (index) {

    const src = jQuery(this).attr('src');
    const poster = jQuery(this).attr('poster');
    var title = jQuery(this).attr('data-title');
      if(typeof title == 'undefined'){
         var title = jQuery(this).parent().find('figcaption').text(); 
      }
      if(typeof title == 'undefined'){
          title=document.title;
      }
      
    var link = jQuery(this).attr('data-link');
      if(typeof link == 'undefined'){
          link=document.URL;
      }
      
    var sharetitle = title+' %0D%0A '+src;

    var id, getControls, replacementMarkup;

    if (jQuery(this).is('audio')) {
      id = `generated-audio-player-${index}`;

      getControls = () => new Audio(jQuery(this).attr('src'));
      replacementMarkup =
        `<div class="stylised-player audio" id='${id}'>
          <div class="stylised-pause" style="display: none;">
            <i class="mdi mdi-pause"></i>
          </div>
          <div class="stylised-play">
            <i class="mdi mdi-play"></i>
          </div>

          <p class="status" style="visibility: hidden;">Loading...</p>

          <div class="stylised-time-wrapper">
            <div class="stylised-time-progress" style="width: 0%;"></div>
          </div>
          
          <div class="stylised-restart" style="display: none;"></div>
          <div class="stylised-share fr" style="margin-right: 3px;" >
            <a  href="whatsapp://send?text=${sharetitle}" data-action="share/whatsapp/share" ><i class="mdi mdi-share-variant" ></i></a>
          </div>
          <div class="stylised-download fr" style="margin-right: 3px;" >
            <a download href="${src}" title="دریافت فایل" ><i class="mdi mdi-download" ></i></a>
          </div>

        </div>`;

    } else if (jQuery(this).is('video')) {
      id = `generated-video-player-${index}`;
      getControls = () => document.getElementById(id + '-screen');
      replacementMarkup =
        `<video class="row" height="auto" src="${src}" poster="${poster}" id='${id}-screen'  preload="none" ></video>
         <div class="stylised-player row borderlight video" id='${id}'>
          <div class="stylised-pause" style="display: none;">
            <i class="mdi mdi-pause"></i>
          </div>
          <div class="stylised-play">
            <i class="mdi mdi-play"></i>
          </div>

          <p class="status" style="visibility: hidden;">Loading...</p>

          <div class="stylised-time-wrapper">
            <div class="stylised-time-progress" style="width: 0%;"></div>
          </div>


          <div class="stylised-restart" style="display: none;"></div>
          <div class="stylised-share fr" style="margin-right: 3px;" >
            <a  href="whatsapp://send?text=${sharetitle}" data-action="share/whatsapp/share" ><i class="mdi mdi-share-variant" ></i></a>
          </div>
          <div class="stylised-download fr" style="margin-right: 3px;" >
            <a download href="${src}" title="دریافت فایل" ><i class="mdi mdi-download" ></i></a>
          </div>
            
            <a href="${link}" title="${title}" class="tooltip padding row taj">
                <h2 class="white-space row taj" style="font-size:18px;direction:rtl;"> ${title} </h2>
            </a>

        </div>`;

    } else {
      console.warn("Element detected was not of type AUDIO or VIDEO and is not supported.");
      return;
    }

    jQuery(this).replaceWith(replacementMarkup);
    var player = { id: id, controls: getControls() };
    jQuery(`#${id} p, #${id} .stylised-time-wrapper, #${id} .stylised-time-progress`).click((e) => playFromPosition(e, id));
    jQuery(`#${id} .stylised-pause`).click(() => pause(id));
    jQuery(`#${id} .stylised-play`).click(() => play(id));
    jQuery(`#${id} .stylised-restart`).click(() => restart(id));

    player.controls.ontimeupdate = () => { updateReadout(player); };
    player.controls.onloadedmetadata = () => { updateReadout(player); };
    player.controls.onseeking = () => { jQuery(`#${id} p`).text("Loading..."); };
    player.controls.onseeked = () => { updateReadout(player); };
    player.controls.onended = () => {
       restart(id);
    };
    players.push(player);
  });
};