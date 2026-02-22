import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace block by block using string.replace
replacements = [
    (
        '''<li><a href="#home">Home</a></li>
                <li><a href="#about">Global Network</a></li>
                <li class="dropdown">
                    <a href="#services">Premium Services <i class="fa-solid fa-chevron-down" style="font-size: 0.8em; margin-left: 5px;"></i></a>
                    <ul class="dropdown-menu">
                        <li><a href="#service-1">I. Seamless Incorporation</a></li>
                        <li><a href="#service-2">II. Global Business Matching</a></li>
                        <li><a href="#service-3">III. VVIP Concierge & Protocol</a></li>
                    </ul>
                </li>
                <li><a href="#partners">Expertise</a></li>
            </ul>
            <a href="#contact" class="btn-primary nav-btn">Consultation</a>''',
        '''<li><a href="#home" data-i18n="nav_home">Home</a></li>
                <li><a href="#about" data-i18n="nav_network">Global Network</a></li>
                <li class="dropdown">
                    <a href="#services"><span data-i18n="nav_services">Premium Services</span> <i class="fa-solid fa-chevron-down" style="font-size: 0.8em; margin-left: 5px;"></i></a>
                    <ul class="dropdown-menu">
                        <li><a href="#service-1" data-i18n="nav_svc1">I. Seamless Incorporation</a></li>
                        <li><a href="#service-2" data-i18n="nav_svc2">II. Global Business Matching</a></li>
                        <li><a href="#service-3" data-i18n="nav_svc3">III. VVIP Concierge & Protocol</a></li>
                    </ul>
                </li>
                <li><a href="#partners" data-i18n="nav_expertise">Expertise</a></li>
            </ul>
            <div class="nav-right" style="display: flex; align-items: center; gap: 20px;">
                <div class="lang-selector dropdown">
                    <a href="#" id="current-lang" style="font-weight: 500;"><i class="fa-solid fa-globe"></i> KOR <i class="fa-solid fa-chevron-down" style="font-size: 0.8em; margin-left: 5px;"></i></a>
                    <ul class="dropdown-menu lang-menu" style="min-width: 150px;">
                        <li><a href="#" data-lang="ko">한국어 (KOR)</a></li>
                        <li><a href="#" data-lang="en">English (ENG)</a></li>
                        <li><a href="#" data-lang="ja">日本語 (JPN)</a></li>
                        <li><a href="#" data-lang="zh">中文 (CHN)</a></li>
                        <li><a href="#" data-lang="vi">Tiếng Việt (VIE)</a></li>
                    </ul>
                </div>
                <a href="#contact" class="btn-primary nav-btn" data-i18n="nav_consultation">Consultation</a>
            </div>'''
    ),
    (
        '''<p class="hero-subtitle">The Ultimate Business & Lifestyle Solution</p>
            <h1 class="hero-title">글로벌 비즈니스의 격을 높이다</h1>
            <p class="hero-desc">
                단순한 진출을 넘어 성공을 담보하는 파트너십.<br>
                아시아 주요 4개국(한국, 중국, 베트남, 일본) 기반의 압도적인 인프라로<br>
                법인 설립부터 VVIP 의전까지 당신의 품격에 맞는 1:1 맞춤형 통합 솔루션을 제공합니다.
            </p>
            <div class="hero-actions">
                <a href="#services" class="btn-primary">서비스 알아보기</a>
                <a href="#contact" class="btn-secondary">프라이빗 상담 예약</a>
            </div>''',
        '''<p class="hero-subtitle" data-i18n="hero_sub">The Ultimate Business & Lifestyle Solution</p>
            <h1 class="hero-title" data-i18n="hero_title">글로벌 비즈니스의 격을 높이다</h1>
            <p class="hero-desc" data-i18n="hero_desc">
                단순한 진출을 넘어 성공을 담보하는 파트너십.<br>
                아시아 주요 4개국(한국, 중국, 베트남, 일본) 기반의 압도적인 인프라로<br>
                법인 설립부터 VVIP 의전까지 당신의 품격에 맞는 1:1 맞춤형 통합 솔루션을 제공합니다.
            </p>
            <div class="hero-actions">
                <a href="#services" class="btn-primary" data-i18n="hero_btn1">서비스 알아보기</a>
                <a href="#contact" class="btn-secondary" data-i18n="hero_btn2">프라이빗 상담 예약</a>
            </div>'''
    ),
    (
        '''<h2 class="section-title">Asia's Premier Network</h2>
                <div class="heading-line"></div>
                <p class="section-subtitle">경계를 허무는 완벽한 비즈니스 커버리지</p>''',
        '''<h2 class="section-title" data-i18n="net_title">Asia's Premier Network</h2>
                <div class="heading-line"></div>
                <p class="section-subtitle" data-i18n="net_sub">경계를 허무는 완벽한 비즈니스 커버리지</p>'''
    ),
    (
        '''<div class="card-content">
                        <h3>Korea</h3>
                        <p>서울 비즈니스 허브 연계, K-컬처 및 프리미엄 의전</p>
                    </div>''',
        '''<div class="card-content">
                        <h3 data-i18n="net_kr_title">Korea</h3>
                        <p data-i18n="net_kr_desc">서울 비즈니스 허브 연계, K-컬처 및 프리미엄 의전</p>
                    </div>'''
    ),
    (
        '''<div class="card-content">
                        <h3>China</h3>
                        <p>상하이·베이징 거점, 압도적인 꽌시(관계) 기반 파트너십 매칭</p>
                    </div>''',
        '''<div class="card-content">
                        <h3 data-i18n="net_cn_title">China</h3>
                        <p data-i18n="net_cn_desc">상하이·베이징 거점, 압도적인 꽌시(관계) 기반 파트너십 매칭</p>
                    </div>'''
    ),
    (
        '''<div class="card-content">
                        <h3>Vietnam</h3>
                        <p>동남아시아 신흥 시장 진출, 제조/IT 투자 및 빠른 법인 설립</p>
                    </div>''',
        '''<div class="card-content">
                        <h3 data-i18n="net_vn_title">Vietnam</h3>
                        <p data-i18n="net_vn_desc">동남아시아 신흥 시장 진출, 제조/IT 투자 및 빠른 법인 설립</p>
                    </div>'''
    ),
    (
        '''<div class="card-content">
                        <h3>Japan</h3>
                        <p>도쿄 중심 프라이빗 VVIP 네트워크 및 하이엔드 럭셔리 레저</p>
                    </div>''',
        '''<div class="card-content">
                        <h3 data-i18n="net_jp_title">Japan</h3>
                        <p data-i18n="net_jp_desc">도쿄 중심 프라이빗 VVIP 네트워크 및 하이엔드 럭셔리 레저</p>
                    </div>'''
    ),
    (
        '''<h2 class="section-title">Exclusive Services</h2>
                <div class="heading-line"></div>
                <p class="section-subtitle">비즈니스 셋업부터 최상위 라이프스타일 케어까지, 타협 없는 전문성</p>''',
        '''<h2 class="section-title" data-i18n="svc_title">Exclusive Services</h2>
                <div class="heading-line"></div>
                <p class="section-subtitle" data-i18n="svc_sub">비즈니스 셋업부터 최상위 라이프스타일 케어까지, 타협 없는 전문성</p>'''
    ),
    (
        '''<h3 class="service-name">I. Seamless Incorporation<br><span>초격차 법인 설립 솔루션</span></h3>
                        <p class="service-desc">
                            해외 시장 진출의 첫 단추, 완벽하게 채워드립니다. 글로벌 대형 로펌 및 회계법인 네트워크(EY, PwC 수준의 공신력)와 Stripe Atlas, Firstbase 등 검증된 최적의 툴을 활용하여 신속하고 리스크 없는 법인 설립(Incorporation) 절차를 안내합니다.
                        </p>
                        <ul class="service-list">
                            <li><i class="fa-solid fa-check"></i> 1:1 맞춤형 지배구조 설계 및 조세 최적화 플랜</li>
                            <li><i class="fa-solid fa-check"></i> 현지 법인 설립 대행 및 라이센스 취득 올인원 서비스</li>
                            <li><i class="fa-solid fa-check"></i> 뱅킹 셋업, 오피스 공간 어레인지 및 초기 채용 지원</li>
                        </ul>''',
        '''<h3 class="service-name" data-i18n="svc1_title">I. Seamless Business Setup<br><span>초격차 비즈니스 셋업 솔루션</span></h3>
                        <p class="service-desc" data-i18n="svc1_desc">
                            해외 진출 시 직면하는 복잡한 규제와 행정적 장벽, 완벽하게 해소해 드립니다. 글로벌 최고 수준의 공신력을 갖춘 로펌 및 회계법인 네트워크와 검증된 최적의 툴을 활용하여 신속하고 리스크 없는 사업 기반 구축 절차를 안내합니다.
                        </p>
                        <ul class="service-list">
                            <li data-i18n="svc1_l1"><i class="fa-solid fa-check"></i> 1:1 맞춤형 지배구조 설계 및 조세 최적화 플랜</li>
                            <li data-i18n="svc1_l2"><i class="fa-solid fa-check"></i> 현지 법인 설립 대행 및 라이센스 취득 올인원 서비스</li>
                            <li data-i18n="svc1_l3"><i class="fa-solid fa-check"></i> 뱅킹 셋업, 오피스 공간 어레인지 및 초기 채용 지원</li>
                        </ul>'''
    ),
    (
        '''<h3 class="service-name">II. Global Business Matching<br><span>비즈니스 발굴 및 서비스 파트너 연결</span></h3>
                        <p class="service-desc">
                            Lava IP, Prime Consultancy 등의 심도 있는 시장 분석 및 파트너 발굴 노하우를 바탕으로, 단순 소개가 아닌 실질적 수익 모델을 창출하는 'B2B 미팅 및 JV 매칭'을 제공합니다.
                        </p>
                        <ul class="service-list">
                            <li><i class="fa-solid fa-check"></i> C-Level 다이렉트 미팅 세팅 및 투자자–스타트업 얼라이언스</li>
                            <li><i class="fa-solid fa-check"></i> 검증된 현지 디스트리뷰터, 벤더, 잠재 고객사 리드 제너레이션</li>
                            <li><i class="fa-solid fa-check"></i> M&A 및 현지 파트너십 협상 전 과정 전략 자문</li>
                        </ul>''',
        '''<h3 class="service-name" data-i18n="svc2_title">II. Global Business Matching<br><span>비즈니스 발굴 및 서비스 파트너 연결</span></h3>
                        <p class="service-desc" data-i18n="svc2_desc">
                            심도 있는 시장 분석 및 파트너 발굴 노하우를 바탕으로, 단순 소개가 아닌 실질적 수익 모델을 창출하는 'B2B 미팅 및 JV 매칭'을 제공합니다.
                        </p>
                        <ul class="service-list">
                            <li data-i18n="svc2_l1"><i class="fa-solid fa-check"></i> C-Level 다이렉트 미팅 세팅 및 투자자–스타트업 얼라이언스</li>
                            <li data-i18n="svc2_l2"><i class="fa-solid fa-check"></i> 검증된 현지 디스트리뷰터, 벤더, 잠재 고객사 리드 제너레이션</li>
                            <li data-i18n="svc2_l3"><i class="fa-solid fa-check"></i> M&A 및 현지 파트너십 협상 전 과정 전략 자문</li>
                        </ul>'''
    ),
    (
        '''<h3 class="service-name">III. VVIP Concierge & Protocol<br><span>최상위 에스코트 및 하이엔드 의전</span></h3>
                        <p class="service-desc">
                            비즈니스의 마침표는 품격 있는 호스피탈리티입니다. The Billionaire Concierge, Vivo Asia Group 수준의 완벽한 럭셔리 컨시어지로, 당신과 귀하의 귀빈을 위한 맞춤형 코퍼레이트 이벤트 및 밀착 의전을 수행합니다.
                        </p>
                        <ul class="service-list">
                            <li><i class="fa-solid fa-check"></i> 공항 VIP 패스트트랙, 프라이빗 리무진 대기 및 경찰/사설 경호 에스코트</li>
                            <li><i class="fa-solid fa-check"></i> 미쉐린 스타 다이닝, 익스클루시브 프라이빗 파티, 요트/전세기 대관</li>
                            <li><i class="fa-solid fa-check"></i> 하이엔드 기업 행사기획, 레드카펫 의전 및 1:1 라이프스타일 케어</li>
                        </ul>''',
        '''<h3 class="service-name" data-i18n="svc3_title">III. VVIP Concierge & Protocol<br><span>최상위 에스코트 및 하이엔드 의전</span></h3>
                        <p class="service-desc" data-i18n="svc3_desc">
                            비즈니스의 마침표는 품격 있는 호스피탈리티입니다. 완벽한 럭셔리 컨시어지로, 당신과 귀하의 귀빈을 위한 맞춤형 코퍼레이트 이벤트 및 밀착 의전을 수행합니다.
                        </p>
                        <ul class="service-list">
                            <li data-i18n="svc3_l1"><i class="fa-solid fa-check"></i> VVIP 전용 프라이빗 리무진 대기 및 VIP 밀착 에스코트</li>
                            <li data-i18n="svc3_l2"><i class="fa-solid fa-check"></i> 미쉐린 스타 다이닝, 익스클루시브 프라이빗 파티, 요트/전세기 대관</li>
                            <li data-i18n="svc3_l3"><i class="fa-solid fa-check"></i> 하이엔드 기업 행사기획, 레드카펫 의전 및 1:1 라이프스타일 케어</li>
                        </ul>'''
    ),
    (
        '''<h2 class="section-title">The Masterpiece Combination</h2>
                <div class="heading-line"></div>
                <p class="section-subtitle">각 분야 최고 수준의 전문성을 통합 제공합니다</p>''',
        '''<h2 class="section-title" data-i18n="ptn_title">The Masterpiece Combination</h2>
                <div class="heading-line"></div>
                <p class="section-subtitle" data-i18n="ptn_sub">각 분야 최고 수준의 전문성을 통합 제공합니다</p>'''
    ),
    (
        '''<h4>Top-Tier <br>Legal & Finance</h4>
                    <p>글로벌 회계 및 법무 네트워크를 통해<br>가장 빠르고 합법적인<br>법인 설립(Incorporation) 모델 완성</p>''',
        '''<h4 data-i18n="ptn1_title">Top-Tier <br>Legal & Finance</h4>
                    <p data-i18n="ptn1_desc">글로벌 회계 및 법무 네트워크를 통해<br>가장 빠르고 합법적인<br>법인 설립(Incorporation) 모델 완성</p>'''
    ),
    (
        '''<h4>Actionable <br>Business Matching</h4>
                    <p>현지 심층 리서치에 기반한<br>공격적이고 실현 가능한<br>로컬 비즈니스 파트너 1:1 세팅</p>''',
        '''<h4 data-i18n="ptn2_title">Actionable <br>Business Matching</h4>
                    <p data-i18n="ptn2_desc">현지 심층 리서치에 기반한<br>공격적이고 실현 가능한<br>로컬 비즈니스 파트너 1:1 세팅</p>'''
    ),
    (
        '''<h4>Executive <br>Hospitality</h4>
                    <p>정확한 동선, 완벽한 보안, <br>그리고 압도적인 파티 및 다이닝 등<br>VVIP 코퍼레이트 컨시어지</p>''',
        '''<h4 data-i18n="ptn3_title">Executive <br>Hospitality</h4>
                    <p data-i18n="ptn3_desc">정확한 동선, 완벽한 보안, <br>그리고 압도적인 파티 및 다이닝 등<br>VVIP 코퍼레이트 컨시어지</p>'''
    ),
    (
        '''<h2>프라이빗 비즈니스의 첫 걸음</h2>
                    <p>오직 초대받은, 혹은 검증된 리더들만을 위한 맞춤 프로세스입니다. 당신이 원하시는 서비스 국가와 구체적인 목표를 남겨주시면, 전문 Account Director가 24시간 이내에 가장 정교한 마스터플랜을 제안합니다.</p>
                    
                    <div class="contact-details">
                        <div class="detail-item">
                            <i class="fa-solid fa-map-location-dot"></i>
                            <div>
                                <strong>Service Areas</strong>
                                <span>Seoul | Beijing/Shanghai | Hanoi/HCMC | Tokyo</span>
                            </div>
                        </div>
                        <div class="detail-item">
                            <i class="fa-solid fa-envelope"></i>
                            <div>
                                <strong>Email</strong>
                                <span>vip@globalprestige.co</span>
                            </div>
                        </div>
                        <div class="detail-item">
                            <i class="fa-solid fa-phone"></i>
                            <div>
                                <strong>Direct Concierge</strong>
                                <span>+82 (0)2 VIP LINE</span>
                            </div>
                        </div>
                    </div>''',
        '''<h2 data-i18n="cnt_title">프라이빗 비즈니스의 첫 걸음</h2>
                    <p data-i18n="cnt_desc">오직 초대받은, 혹은 검증된 리더들만을 위한 맞춤 프로세스입니다. 당신이 원하시는 서비스 국가와 구체적인 목표를 남겨주시면, 전문 Account Director가 24시간 이내에 가장 정교한 마스터플랜을 제안합니다.</p>
                    
                    <div class="contact-details">
                        <div class="detail-item">
                            <i class="fa-solid fa-map-location-dot"></i>
                            <div>
                                <strong data-i18n="cnt_areas_title">Service Areas</strong>
                                <span data-i18n="cnt_areas_val">Seoul | Beijing/Shanghai | Hanoi/HCMC | Tokyo</span>
                            </div>
                        </div>
                        <div class="detail-item">
                            <i class="fa-solid fa-envelope"></i>
                            <div>
                                <strong data-i18n="cnt_email">Email</strong>
                                <span>vip@globalprestige.co</span>
                            </div>
                        </div>
                        <div class="detail-item">
                            <i class="fa-solid fa-phone"></i>
                            <div>
                                <strong data-i18n="cnt_phone">Direct Concierge</strong>
                                <span>+82 (0)2 VIP LINE</span>
                            </div>
                        </div>
                    </div>'''
    ),
    (
        '''<label for="name">성함 / Name</label>
                            <input type="text" id="name" required placeholder="이름을 기입해주세요">
                        </div>
                        <div class="form-group">
                            <label for="company">소속 / Company</label>
                            <input type="text" id="company" required placeholder="기업명 및 직함을 기입해주세요">
                        </div>
                        <div class="form-group">
                            <label for="email">이메일 / Email</label>
                            <input type="email" id="email" required placeholder="연락 받으실 이메일">
                        </div>
                        <div class="form-group">
                            <label for="country">희망 국가 (선택)</label>
                            <select id="country">
                                <option value="" disabled selected>국가를 선택해주세요</option>
                                <option value="korea">대한민국 (Korea)</option>
                                <option value="china">중국 (China)</option>
                                <option value="vietnam">베트남 (Vietnam)</option>
                                <option value="japan">일본 (Japan)</option>
                                <option value="multiple">다중 국가 (Multiple)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>주요 관심 서비스 (중복 가능)</label>
                            <div class="checkbox-group">
                                <label><input type="checkbox" name="interest"> 법인 설립 및 조세 자문</label>
                                <label><input type="checkbox" name="interest"> 파트너 매칭 및 리드 제너레이션</label>
                                <label><input type="checkbox" name="interest"> VIP 의전 및 프라이빗 보안</label>
                                <label><input type="checkbox" name="interest"> 럭셔리 코퍼레이트 이벤트/파티</label>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="message">요청 사항 / Message</label>
                            <textarea id="message" rows="4" placeholder="상세한 요청 내용이나 희망 상담 일정을 남겨주세요"></textarea>
                        </div>
                        <button type="submit" class="submit-btn btn-primary">프라이빗 상담 신청 <i class="fa-solid fa-arrow-right"></i></button>''',
        '''<label for="name" data-i18n="form_name">성함 / Name</label>
                            <input type="text" id="name" required placeholder="이름을 기입해주세요" data-i18n-ph="form_name_ph">
                        </div>
                        <div class="form-group">
                            <label for="company" data-i18n="form_company">소속 / Company</label>
                            <input type="text" id="company" required placeholder="기업명 및 직함을 기입해주세요" data-i18n-ph="form_company_ph">
                        </div>
                        <div class="form-group">
                            <label for="email" data-i18n="form_email">이메일 / Email</label>
                            <input type="email" id="email" required placeholder="연락 받으실 이메일" data-i18n-ph="form_email_ph">
                        </div>
                        <div class="form-group">
                            <label for="country" data-i18n="form_country">희망 국가 (선택)</label>
                            <select id="country">
                                <option value="" disabled selected data-i18n="form_country_ph">국가를 선택해주세요</option>
                                <option value="korea" data-i18n="form_country_kr">대한민국 (Korea)</option>
                                <option value="china" data-i18n="form_country_cn">중국 (China)</option>
                                <option value="vietnam" data-i18n="form_country_vn">베트남 (Vietnam)</option>
                                <option value="japan" data-i18n="form_country_jp">일본 (Japan)</option>
                                <option value="multiple" data-i18n="form_country_multi">다중 국가 (Multiple)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label data-i18n="form_interests">주요 관심 서비스 (중복 가능)</label>
                            <div class="checkbox-group">
                                <label><input type="checkbox" name="interest"> <span data-i18n="form_int1">법인 설립 및 조세 자문</span></label>
                                <label><input type="checkbox" name="interest"> <span data-i18n="form_int2">파트너 매칭 및 리드 제너레이션</span></label>
                                <label><input type="checkbox" name="interest"> <span data-i18n="form_int3">VIP 의전 및 프라이빗 보안</span></label>
                                <label><input type="checkbox" name="interest"> <span data-i18n="form_int4">럭셔리 코퍼레이트 이벤트/파티</span></label>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="message" data-i18n="form_msg">요청 사항 / Message</label>
                            <textarea id="message" rows="4" placeholder="상세한 요청 내용이나 희망 상담 일정을 남겨주세요" data-i18n-ph="form_msg_ph"></textarea>
                        </div>
                        <button type="submit" class="submit-btn btn-primary" data-i18n="form_submit">프라이빗 상담 신청 <i class="fa-solid fa-arrow-right"></i></button>'''
    ),
    (
        '''<p>The Ultimate Partner for Global Elite Expansion.</p>
            </div>
            <div class="footer-links">
                <a href="#">Privacy Policy</a>
                <a href="#">Terms of Service</a>
                <a href="#">Client Access Portal</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Global Prestige Network. All Rights Reserved. Restricted to Authorized Personnel & VIP Clients.</p>
        </div>''',
        '''<p data-i18n="footer_desc">The Ultimate Partner for Global Elite Expansion.</p>
            </div>
            <div class="footer-links">
                <a href="#" data-i18n="footer_p1">Privacy Policy</a>
                <a href="#" data-i18n="footer_p2">Terms of Service</a>
                <a href="#" data-i18n="footer_p3">Client Access Portal</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p data-i18n="footer_copy">&copy; 2026 Global Prestige Network. All Rights Reserved. Restricted to Authorized Personnel & VIP Clients.</p>
        </div>'''
    ),
    (
        '''<script src="script.js"></script>''',
        '''<script src="i18n.js"></script>\n    <script src="script.js"></script>'''
    )
]

# Apply replacements
updated = html
for old_s, new_s in replacements:
    updated = updated.replace(old_s, new_s)
    
if updated != html:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated)
    print("Replacements successful!")
else:
    print("No changes made. Please verify replacements.")
