Component({
  data: {
    modalVisible: false,
  },
  properties: {
    visible: Boolean,
    imageSrc: String,
  },
  observers: {
    visible: function (visible) {
      this.setData({
        modalVisible: visible
      });
    },
  },
  methods: {
    onClose() {
      this.setData({ modalVisible: false });
    }
  }
});
