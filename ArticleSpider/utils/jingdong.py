# coding=utf-8
__author__ = "alvin"
__date__ = "2018/4/10 17:03"

import requests
s = requests.session()
headers = {
        'Host': 'www.jd.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.140 Safari/537.36',
        # 'Cookie': '__jda=122270672.15233509065301289182773.1523350907.1523350907.1523350907.1; __jdc=122270672; '
        #           '__jdv=122270672|baidu|-|organic|not set|1523350906531; o2Control=webp; __jdu=15233509065301289182773; wlfstk_smdl=r9wv1qsw20ya3nkb4pdna3ib0gt04h9w; _jrda=1; _jrdb=1523350923428; TrackID=1Xa5Qc9jVnYmC1A1KP6PDS0A5Ep13Ddxgr2R4Q5SpZIykVESN-alnNiybHZl3yfUIPKgqM-hJV04k8t6hxlt3dCIMoZZiuzjGK1faLpcyHqs; pinId=ogFzxHw7Ax0KXBQfZZf-ASGud-cqMUeO; pin=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; unick=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; _tp=J6Xlo1kzmxTjJtsqEpR5WLzS88BZxRj9wvb8cnwR9GxuJMZoSzQsigPnU17WPSBl3Ssr%2B98SaUks%0D%0AXATHs8kcrQ%3D%3D; _pst=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; ceshi3.com=000; PCSYCityID=2; 3AB9D23F7A4B3C9B=KEPC2U4NHYKXHW3EVYPL2M65ZUF247EFIQLOAQ73ZRQZEARPMNNUFNJUR6DPBPBRAHYY4J2JL2FSAD5REXZPOHFQCM; thor=5CBB2CBBDE2287D267D2E44EC58AF80B43AF366FA473C560C2C3A03D48A5BDDE74FA2D223E0FC37A202EB4B55EE9A32F3FA32645943DEC2CE532804985A3949EEF6EEAD0906606972376936D9A09E8634EB5D85D686C878EA014FA820FD1D18414CF7DC6B01C4F969AE85815E9016A67E8FF6E6D4D8D60BF825F9BAA7BC8A8091DCFD342443A0DE1CE331FF6A3FC653A; __jdb=122270672.10.15233509065301289182773|1.1523350907; user-key=2c206c66-e96f-45e5-854a-b164b55252a0; cn=0',
        # 'Cookie': 'o2Control=; user-key=097c597d-7391-488c-9477-b5d4686e8f69; cn=0; __jda=122270672.1523352230475382942493.1523352230.1523352230.1523352230.1; __jdb=122270672.7.1523352230475382942493|1.1523352230; __jdc=122270672; __jdv=122270672|direct|-|none|-|1523352230485; __jdu=1523352230475382942493; PCSYCityID=2; wlfstk_smdl=sntggojxstlkt3kgf0c7lzjs83hgwsao; _jrda=1; _jrdb=1523352235544; 3AB9D23F7A4B3C9B=ZTUQOA5QHGUSQ44HDXKQVZEG3AY7LTTPMAB6XX34ZYANRNZEKJOWGIO2HDLFAIKW2Q4HGMY5O3RYVIYOGDXYZVJAOI; TrackID=1DCDDJYKXUskJRVRMgRREallvU30o-lIrtSrdevcG6AdUJt43x3k3UE1pp88CjDehCDnss8KEXupMHhs6LVKsK5mKIguWfApI2LUSJfqtafw3z7NkFJf0V_lbfc_vvj3zi3WznMYdauLaVRG8lUxv5g; pinId=ogFzxHw7Ax0KXBQfZZf-ASGud-cqMUeO; pin=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; unick=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; thor=606F2E6FA1C3B3EAEEBC41879F1E3CC04E0F2AE059673760B29A7C048D2DA8520D64D6670E2FB137B92F8A5E40ABF1A2EF26C78C7529FCC846795736E7CA42414DA72865BA91A253A8864D185E4A85DA999375C207DFF2A7C4D815D68CF3494AF6F8D02A7D1446080740B30E8928E78C2CEDB26460A57F507291E2C0C8652B0DED45E4DC969879625B5F00E28E49DD6A; _tp=J6Xlo1kzmxTjJtsqEpR5WLzS88BZxRj9wvb8cnwR9GxuJMZoSzQsigPnU17WPSBl3Ssr%2B98SaUks%0D%0AXATHs8kcrQ%3D%3D; _pst=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; ceshi3.com=000'
        # 'Cookie': '__jda=122270672.15233509065301289182773.1523350907.1523350907.1523350907.1; __jdv=122270672|baidu|-|organic|not set|1523350906531; o2Control=webp; __jdu=15233509065301289182773; _jrda=1; TrackID=1Xa5Qc9jVnYmC1A1KP6PDS0A5Ep13Ddxgr2R4Q5SpZIykVESN-alnNiybHZl3yfUIPKgqM-hJV04k8t6hxlt3dCIMoZZiuzjGK1faLpcyHqs; pinId=ogFzxHw7Ax0KXBQfZZf-ASGud-cqMUeO; pin=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; unick=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; _tp=J6Xlo1kzmxTjJtsqEpR5WLzS88BZxRj9wvb8cnwR9GxuJMZoSzQsigPnU17WPSBl3Ssr%2B98SaUks%0D%0AXATHs8kcrQ%3D%3D; _pst=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; PCSYCityID=2; 3AB9D23F7A4B3C9B=KEPC2U4NHYKXHW3EVYPL2M65ZUF247EFIQLOAQ73ZRQZEARPMNNUFNJUR6DPBPBRAHYY4J2JL2FSAD5REXZPOHFQCM; user-key=2c206c66-e96f-45e5-854a-b164b55252a0; cn=1; ipLoc-djd=1-72-2819; __jdb=122270672.20.15233509065301289182773|1.1523350907; __jdc=122270672'
        'Cookie': '__jda=122270672.15233509065301289182773.1523350907.1523350907.1523350907.1; __jdv=122270672|baidu|-|organic|not set|1523350906531; o2Control=webp; __jdu=15233509065301289182773; pinId=ogFzxHw7Ax0KXBQfZZf-ASGud-cqMUeO; pin=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; unick=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; _tp=J6Xlo1kzmxTjJtsqEpR5WLzS88BZxRj9wvb8cnwR9GxuJMZoSzQsigPnU17WPSBl3Ssr%2B98SaUks%0D%0AXATHs8kcrQ%3D%3D; _pst=%E6%AD%A3%E4%B9%89%E7%BA%A2%E9%A2%86%E5%B7%BE1318; PCSYCityID=2; user-key=2c206c66-e96f-45e5-854a-b164b55252a0; cn=1; ipLoc-djd=1-72-2819; __jdc=122270672; 3AB9D23F7A4B3C9B=XKNIL4JEAM5UXAOSRI4RSBLVQWLTL5CAQZB5DIIDVUIVSS7V62TYJLTJUNICCGPVJ2JM2LEOSH4RBZ4OJLXBZJJV24; _jrda=2; _jrdb=1523352906166; wlfstk_smdl=mt7zh7kzfj3jdve5p8ichny1ix98m6p8; TrackID=1lkDPllBm3ThgO5a5sd6YsowhBUzRdRBW0Dd4QS7qZl7XIwIl4XGr6W46p2nktlUntlAsdWe6h4TOq5AGSWmkxD5CQBZ4CPfnVt6EInddLAk; ceshi3.com=000; __jdb=122270672.24.15233509065301289182773|1.1523350907; thor=BBC36AF8B96EEBD00720B67233C688C9C61E7C4827557546B5D5E89F53741547092F75390D50DA0B11350DF7527AC85EB797011C774412DDCFFA296A0E993D2906DEE60922402AA60B99AAC7FEA0C0B2D4DEC1906A8BFC85CE80A3B6A6C98B8B86259A04BF483D8EC023E7139FD9319C02C5B061C953E4FD4528DDF6A6941CD0C9E5C9F7DB4B93CF549EE95B21F4D22E'
}
response = s.get('https://www.jd.com/', headers=headers, verify=False,
                 allow_redirects=False)
# with open("zhihu.index", "wb") as f:
#     f.write(response.text.encode('utf8'))
# res = s.get('https://www.zhihu.com/settings/profile',headers=headers)
res = s.get('https://cart.jd.com/cart.action', headers=headers, verify=False)
print(res.text)