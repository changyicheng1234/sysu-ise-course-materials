Component({
  data: {
    modalVisible: false,
    tipText: '云开发>云模板>模板中心',
  },
  properties: {
    installModulePageTitleProps: String,
    modalVisibleProps: Boolean,
    tipTextProps: String,
    installModuleNameProps: String,
  },
  observers: {
    modalVisibleProps: function (modalVisibleProps) {
      this.setData({
        modalVisible: modalVisibleProps,
      });
    },
    tipTextProps: function (tipTextProps) {
      this.setData({
        tipText: tipTextProps,
      });
    },
  },
  methods: {
    hideModal() {
      if (this.data.modalVisible) {
        this.setData({
          modalVisible: false,
        });
      }
    },
    onViewDetail() {
      this.hideModal();
      wx.navigateTo({
        url: `/pages/cloudbaseModuleInstallTips/index?moduleName=${this.properties.installModuleNameProps}&title=${this.properties.installModulePageTitleProps}`,
      });
    },
  },
});
