package com.bankcomm.controllers;

import com.bankcomm.domain.News;
import com.bankcomm.domain.Pager;
import com.bankcomm.services.NewsService;
import org.apache.tomcat.util.codec.binary.Base64;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import java.util.Optional;

@Controller
public class NewsController {
    private static final int BUTTONS_TO_SHOW = 5;
    private static final int INITIAL_PAGE = 0;
    private static final int INITIAL_PAGE_SIZE = 30;
    private static final int[] PAGE_SIZES = {5, 10, 20};

    private NewsService newsService;

    @Autowired
    public void setNewsService(NewsService newsService) {
        this.newsService = newsService;
    }

//    @RequestMapping("/")
//    String index(Model model){
//        model.addAttribute("newsList", newsService.getAllNews());
//        model.addAttribute("topHotNewsList", newsService.getTopHotNews());
//        return "index";
//    }
    @RequestMapping("/")
    public ModelAndView index(@RequestParam("pageSize") Optional<Integer> pageSize, @RequestParam("page") Optional<Integer> page, @RequestParam(value = "type", defaultValue = "金融科技") String type){
        ModelAndView modelAndView = new ModelAndView("index");
        int evalPageSize = pageSize.orElse(INITIAL_PAGE_SIZE);
        int evalPage = (page.orElse(0) < 1) ? INITIAL_PAGE : page.get() - 1;
        Page<News> newsList = newsService.getAllNews(PageRequest.of(evalPage, evalPageSize), type);
        Pager pager = new Pager(newsList.getTotalPages(), newsList.getNumber(), BUTTONS_TO_SHOW);
        modelAndView.addObject("newsList", newsList);
        modelAndView.addObject("topHotNewsList", newsService.getTopHotNews());
        modelAndView.addObject("selectedPageSize", evalPageSize);
        modelAndView.addObject("pageSizes", PAGE_SIZES);
        modelAndView.addObject("pager", pager);
        return modelAndView;
    }

    @RequestMapping(value = "/detail", method = RequestMethod.GET)
    public String showNewsDetail(@RequestParam Integer id, Model model){
        model.addAttribute("topHotNewsList", newsService.getTopHotNews());
        model.addAttribute("news", newsService.getNewsById(id));
        return "detail";
    }

    @RequestMapping(value = "/hot", method = RequestMethod.GET)
    public ModelAndView getAllHotNews(@RequestParam("pageSize") Optional<Integer> pageSize, @RequestParam("page") Optional<Integer> page){
        ModelAndView modelAndView = new ModelAndView("hot");
        int evalPageSize = pageSize.orElse(INITIAL_PAGE_SIZE);
        int evalPage = (page.orElse(0) < 1) ? INITIAL_PAGE : page.get() - 1;
        Page<News> allHotNewsList = newsService.getAllHotNews(PageRequest.of(evalPage, evalPageSize), "1");
        Pager pager = new Pager(allHotNewsList.getTotalPages(), allHotNewsList.getNumber(), BUTTONS_TO_SHOW);
        modelAndView.addObject("allHotNewsList", allHotNewsList);
        modelAndView.addObject("selectedPageSize", evalPageSize);
        modelAndView.addObject("pageSizes", PAGE_SIZES);
        modelAndView.addObject("pager", pager);
        return modelAndView;
    }
}
