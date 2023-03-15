window.Storyteller = {
    uuid: null,
    ready: false,
    init: function() {
        if (this.ready) {
          return;
        }
        this.uuid = this.getUUIDFromCookie();
        if (!this.uuid) {
            this.uuid = this.generateUUID();
            this.setCookie(this.uuid);
            console.log("set cookie with uuid: ", this.uuid);
        }
        this.ready = true;
        if (!window.location.href.includes(this.uuid)) {
          window.location.replace(window.location.origin + "/messages/" + this.uuid);
        }
    },
    generateUUID: function() {
        var d = new Date().getTime();
        if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
            d += performance.now(); //use high-precision timer if available
        }
        return 'xxxxxxxx-xxxx-xxxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = (d + Math.random() * 16) % 16 | 0;
            d = Math.floor(d / 16);
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
    },
    setCookie: function(uuid) {
      document.cookie = "storyteller_id=" + uuid + ";max-age=60*60*24*30;SameSite=None;";
    },
    removeCookie: function() {
        /* deprecating js way of handling cookie since it's unstable in flask app
        document.cookie = "storyteller_id=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        location.reload(); */
        window.location.replace(window.location.origin + "/removeCookie");
    },
    getUUIDFromCookie: function() {
        const cookieValue = document.cookie.split("; ").find((row) => row.startsWith("storyteller_id="))?.split("=")[1];
        return cookieValue;
    },
}
if ("Storyteller" in window) {
    Storyteller.init();
}