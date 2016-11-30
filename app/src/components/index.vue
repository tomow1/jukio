<template>
  <quasar-layout>
    <div slot="header" class="toolbar">
      <!-- opens drawer below -->
      <button class="hide-on-drawer-visible" @click="$refs.drawer.open()">
        <i>menu</i>
      </button>

      <quasar-toolbar-title :padding="3">
        Title
      </quasar-toolbar-title>

      <toggle-button v-model="repeat.selected" :values="repeat.values" v-on:input="toggle(repeat)">
        <i class="text-primary" :class="repeat.values[repeat.selected].class">{{repeat.values[repeat.selected].icon}}</i>
      </toggle-button>
      <toggle-button v-model="shuffle.selected" :values="shuffle.values" v-on:input="toggle(shuffle)">
        <i class="text-primary">{{shuffle.values[shuffle.selected].icon}}</i>
      </toggle-button>
      <toggle-button v-model="consume.selected" :values="consume.values" v-on:input="toggle(consume)">
        <!--img id="pacman" src="~assets/Pacman.svg" /-->
        <i class="text-primary" :class="consume.values[consume.selected].class">{{consume.values[consume.selected].icon}}</i>
      </toggle-button>


    </div>

    <!-- Navigation Tabs
    <quasar-tabs slot="navigation">
      <quasar-tab icon="mail" route="/layout" exact replace>Mails</quasar-tab>
      <quasar-tab icon="alarm" route="/layout/alarm" exact replace>Alarms</quasar-tab>
      <quasar-tab icon="help" route="/layout/help" exact replace>Help</quasar-tab>
    </quasar-tabs>
    -->

    <!-- Drawer -->
    <quasar-drawer ref="drawer">
      <div class="toolbar">
        <quasar-toolbar-title>
          Drawer Title
        </quasar-toolbar-title>
      </div>

      <div class="list no-border platform-delimiter">
        <quasar-drawer-link icon="settings" to="/settings" exact>
          Settings
        </quasar-drawer-link>
      </div>
    </quasar-drawer>


    <div class="layout-view bg-light-grey-4">
      <div class="list item-delimiter bg-white">
        <label class="item" id="autoplay">
          <div class="item-content item-has-secondary">
            <span class="item-label">Autoplay</span>
            <!--quasar-numeric v-model="autoplay.tracks"></quasar-numeric>
            <span class="item-label">tracks</span-->
          </div>
          <div class="item-secondary">
            <quasar-toggle v-model="autoplay.state" v-on:input="autoplay"></quasar-toggle>
          </div>
        </label>
        <div class="item item-link morelink" id="morelike" v-on:click="morelike">
          <div class="item-content item-has-secondary ellipsis">
            <span class="item-label">More like</span>
            <span class="emphasize capitalize">{{nowPlaying.title}}</span>
          </div>
          <i class="item-secondary">audiotrack</i>
        </div>
        <div class="item item-link morelink" id="morefrom" v-on:click="morefrom">
          <div class="item-content item-has-secondary ellipsis">
            <span class="item-label">More from</span>
            <span class="emphasize capitalize">{{nowPlaying.artist}}</span>
          </div>
          <i class="item-secondary">person</i>
        </div>
      </div>
    </div>

    <!-- Footer-->
    <div slot="footer" class="toolbar">
      <button>
        <i>volume_up</i>
      </button>
      <button>
        <i>skip_previous</i>
      </button>
      <button>
        <i>play_arrow</i>
      </button>
      <button>
        <i>skip_next</i>
      </button>
      <button>
        <i>playlist_play</i>
      </button>
    </div>

  </quasar-layout>
</template>

<script>
import ToggleButton from './ToggleButton'
var request = require('superagent')

import { Events } from 'quasar'

export default {
  components: {
    ToggleButton
  },
  data () {
    return {
      shuffle: {
        selected: 0,
        values: [
          { icon: 'shuffle', state: false },
          { icon: 'shuffle', state: true }
        ]
      },
      repeat: {
        selected: 0,
        values: [
          { icon: 'repeat', state: false },
          { icon: 'repeat', state: true },
          { icon: 'repeat_one', state: true },
          { icon: 'filter_1', state: true, class: 's' }
        ]
      },
      consume: {
        selected: 0,
        values: [
          { icon: 'consume', state: false, class: 'j s' },
          { icon: 'consume', state: true, class: 'j s' }
        ]
      },
      autoplay: {
        state: false,
        tracks: 0
      },
      nowPlaying: {
        artist: 'iron maiden',
        title: 'run to the hills'
      }
    }
  },
  created () {
    this.loadData()
    Events.$on('app:visibility', (state) => {
      if (state === 'visible') {
        this.loadData()
      }
    })
    /* setInterval(function () {
      this.loadData()
    }.bind(this), 60000) */
  },
  methods: {
    loadData () {
      request.get('/status').end((err, res) => {
        if (err) throw err
        this.autoplay.state = res.body.autoplay
        this.consume.selected = res.body.consume
        this.shuffle.selected = res.body.random
        if (res.body.repeat === 0 && res.body.single === 0) {
          this.repeat.selected = 0
        }
        else if (res.body.repeat === 1 && res.body.single === 0) {
          this.repeat.selected = 1
        }
        else if (res.body.repeat === 1 && res.body.single === 1) {
          this.repeat.selected = 2
        }
        else if (res.body.repeat === 0 && res.body.single === 1) {
          this.repeat.selected = 3
        }
        this.nowPlaying = res.body.nowPlaying
        // console.log(this.consume)
      })
    },
    toggle (e) {
      var payload = { }
      if (e.values[e.selected].icon === 'remove_from_queue') {
        payload.consume = this.consume.selected === 1
      }
      if (e.values[e.selected].icon === 'shuffle') {
        payload.random = this.shuffle.selected === 1
      }
      if (e.values[e.selected].icon.startsWith('repeat')) {
        payload.repeat = this.repeat.selected >= 1
        payload.single = this.repeat.selected >= 2
      }
      if (e.values[e.selected].icon === 'filter_1') {
        payload.repeat = false
        payload.single = true
      }
      request.post('/controls')
      .send(payload)
      .end((err, res) => {
        if (err) throw err
        this.loadData()
      })
    },
    autoplay () {
      var payload = {
        autoplay: this.autoplay.state
      }
      request.post('/autoplay')
      .send(payload)
      .end((err, res) => {
        if (err) throw err
        this.loadData()
      })
    },
    morelike () {
      var payload = {
        quantity: 5
      }
      request.post('/playmore')
      .send(payload)
      .end((err, res) => {
        if (err) throw err
        this.loadData()
      })
    },
    morefrom () {
      var payload = {
        quantity: 5
      }
      request.post('/playtop')
      .send(payload)
      .end((err, res) => {
        if (err) throw err
        this.loadData()
      })
    }
  }
}
</script>

<style lang="styl">
icomoon-font-path ?= "~assets"
@font-face
  font-family 'jukio'
  src url(icomoon-font-path + '/jukio.eot?e06rt')
  src url(icomoon-font-path + '/jukio.eot?e06rt#iefix') format('embedded-opentype'), url(icomoon-font-path + '/jukio.ttf?e06rt') format('truetype'), url(icomoon-font-path + '/jukio.woff?e06rt') format('woff'), url(icomoon-font-path + '/jukio.svg?e06rt#jukio') format('svg')
  font-weight normal
  font-style normal
// .ios #autoplay .item-content
//   padding 8px 0
.ios .morelink .item-content
  margin-right 48px
i.j
  font-family 'jukio' !important
i.s
  font-size 1rem !important
</style>
