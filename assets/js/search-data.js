// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-projects",
          title: "projects",
          description: "Ongoing research and engineering projects in liquid-metal electronics, wearable bioelectronics, and electrochemical biosensing.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "Curriculum vitae of Chansoo (Charles) Kim — graduate researcher at the BLISS Lab, Yonsei University.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-teaching",
          title: "teaching",
          description: "Courses I have supported as a teaching assistant at Yonsei University.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "news-our-capstone-team-was-selected-as-one-of-eight-outstanding-research-teams-in-electrical-amp-amp-electronic-engineering-where-i-served-as-the-supervising-teaching-assistant",
          title: 'Our capstone team was selected as one of eight Outstanding Research Teams in...',
          description: "",
          section: "News",},{id: "news-the-flexible-pcb-revision-of-the-four-channel-ad5941-sensor-toolkit-came-back-from-fabrication-and-passed-bring-up-analog-front-end-verified-over-ble-on-the-flex-board",
          title: 'The flexible-PCB revision of the four-channel AD5941 sensor toolkit came back from fabrication...',
          description: "",
          section: "News",},{id: "news-abstract-accepted-for-an-oral-presentation-at-the-2026-mrs-fall-meeting-in-boston-symposium-sb13-advancements-in-liquid-metal-science",
          title: 'Abstract accepted for an oral presentation at the 2026 MRS Fall Meeting in...',
          description: "",
          section: "News",},{id: "projects-pda-lm-ink",
          title: 'PDA-LM Ink',
          description: "Sintering-free, primer-free liquid-metal ink via catechol–Ga³⁺ chelation — a 10-minute deep dive",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_project/";
            },},{id: "projects-water-transfer-electronics",
          title: 'Water-Transfer Electronics',
          description: "Hydroprinted liquid-metal circuits transferred onto skin via PVA carrier",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_project/";
            },},{id: "projects-wearable-bci",
          title: 'Wearable BCI',
          description: "A direction I want to work in — non-invasive ear-EEG with soft, liquid-metal contacts",
          section: "Projects",handler: () => {
              window.location.href = "/projects/3_project/";
            },},{id: "projects-pdrn-bio-coating",
          title: 'PDRN Bio-Coating',
          description: "Dual anti-fouling + tissue-regeneration coating for sutures and intramuscular EMG",
          section: "Projects",handler: () => {
              window.location.href = "/projects/4_project/";
            },},{id: "projects-ad5941-ec-sensor-toolkit",
          title: 'AD5941 EC Sensor Toolkit',
          description: "Portable 4-channel electrochemical sensor based on AD5941 + ESP32-C6",
          section: "Projects",handler: () => {
              window.location.href = "/projects/5_project/";
            },},{id: "projects-multimodal-bioelectronics",
          title: 'Multimodal Bioelectronics',
          description: "Combined EC + EMG + neurostim front-end roadmap",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_project/";
            },},{id: "teachings-bio-electrical-electronics-laboratory-바이오전기전자실험",
          title: 'Bio-electrical Electronics Laboratory (바이오전기전자실험)',
          description: "Teaching assistant for the undergraduate hands-on laboratory course on biopotential acquisition, electrochemical sensing, and embedded data acquisition.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/bio-electrical-electronics-lab/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%6E%63%65%39%30%38%30@%79%6F%6E%73%65%69.%61%63.%6B%72", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/charleskim990819", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/charleskim99", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
