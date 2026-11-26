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
          description: "Liquid-metal materials, wearable instruments, and software I have built or contributed to.",
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
          description: "A water-based ink that forms conductive traces as it dries.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_project/";
            },},{id: "projects-water-transfer-electronics",
          title: 'Water-Transfer Electronics',
          description: "A printed circuit transferred onto the back of a hand to light four LEDs.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_project/";
            },},{id: "projects-wearable-bci",
          title: 'Wearable BCI',
          description: "A research direction for recording brain signals around the ear with soft contacts.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/3_project/";
            },},{id: "projects-pdrn-bio-coating",
          title: 'PDRN Bio-Coating',
          description: "Testing a coating for sutures and implanted muscle electrodes.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/4_project/";
            },},{id: "projects-ad5941-ec-sensor-toolkit",
          title: 'AD5941 EC Sensor Toolkit',
          description: "A four-channel portable potentiostat for testing printed electrodes.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/5_project/";
            },},{id: "projects-multimodal-bioelectronics",
          title: 'Multimodal Bioelectronics',
          description: "A concept for combining chemical sensing, muscle recording, and stimulation in one wearable.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_project/";
            },},{id: "projects-research-bottleneck-map",
          title: 'Research Bottleneck Map',
          description: "A Korean-language web app for reading and annotating research limitations reported in paper abstracts.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/bottleneck-map/";
            },},{id: "projects-screen-printed-electrochemical-electrodes",
          title: 'Screen-printed electrochemical electrodes',
          description: "Measuring how consistently soft, printed electrodes work from one device to the next.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/printed-electrodes/";
            },},{id: "projects-liquid-metal-electrodes-for-ecg-and-emg",
          title: 'Liquid-metal electrodes for ECG and EMG',
          description: "Testing printed electrodes for recording heart and muscle signals in a collaborative study.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/pva-liquid-metal-electrodes/";
            },},{id: "projects-stk-revm20-sensor-front-end",
          title: 'STK RevM20 sensor front end',
          description: "A flex-board design for recording three currents and pH simultaneously, with a verification plan.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/stk-revm20/";
            },},{id: "projects-stretchable-emg-circuit",
          title: 'Stretchable EMG circuit',
          description: "A stretchable electrode readout design and an EMG-controlled RC car demonstration.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/stretchable-exg/";
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
