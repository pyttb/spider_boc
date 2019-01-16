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
import org.springframework.web.servlet.mvc.method.annotation.StreamingResponseBody;

import javax.servlet.http.HttpServletResponse;
import java.io.*;
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

    @RequestMapping("/")
    public ModelAndView index(@RequestParam("pageSize") Optional<Integer> pageSize, @RequestParam("page") Optional<Integer> page, @RequestParam(value = "type", defaultValue = "金融科技") String type){
        ModelAndView modelAndView = new ModelAndView("index");
        int evalPageSize = pageSize.orElse(INITIAL_PAGE_SIZE);
        int evalPage = (page.orElse(0) < 1) ? INITIAL_PAGE : page.get() - 1;
        Page<News> newsList = newsService.getAllNews(PageRequest.of(evalPage, evalPageSize), type);
//        for (News news: newsList){
//            if (news.getPdf() != null)
//            {
//                news.setPdf("0".getBytes());
//            }
//        }
        Pager pager = new Pager(newsList.getTotalPages(), newsList.getNumber(), BUTTONS_TO_SHOW);
        modelAndView.addObject("newsList", newsList);
        modelAndView.addObject("topHotNewsList", newsService.getTopHotNews());
        modelAndView.addObject("selectedPageSize", evalPageSize);
        modelAndView.addObject("pageSizes", PAGE_SIZES);
        modelAndView.addObject("pager", pager);
        return modelAndView;
    }

    @RequestMapping(value = "/detail", method = RequestMethod.GET)
    public String showNewsDetail(@RequestParam Integer id, @RequestParam(value = "type", defaultValue = "金融科技") String type, Model model){
        model.addAttribute("topHotNewsList", newsService.getTopHotNews());
        model.addAttribute("recommendNewsList", newsService.getRecommendNewsList(type));
        News news = newsService.getNewsById(id);
//        if (news.getPdf() != null){
//            news.setPdf("0".getBytes());
//        }
        if("行业报告".equals(type)) {
            news.setPdf("0".getBytes());
        }
        model.addAttribute("news", news);
        return "detail";
    }

    @RequestMapping(value = "/hot", method = RequestMethod.GET)
    public ModelAndView getAllHotNews(@RequestParam("pageSize") Optional<Integer> pageSize, @RequestParam("page") Optional<Integer> page){
        ModelAndView modelAndView = new ModelAndView("hot");
        int evalPageSize = pageSize.orElse(INITIAL_PAGE_SIZE);
        int evalPage = (page.orElse(0) < 1) ? INITIAL_PAGE : page.get() - 1;
        Page<News> allHotNewsList = newsService.getAllHotNews(PageRequest.of(evalPage, evalPageSize), "1");
//        for (News news: allHotNewsList){
//            if (news.getPdf() != null)
//            {
//                news.setPdf("0".getBytes());
//            }
//        }
        Pager pager = new Pager(allHotNewsList.getTotalPages(), allHotNewsList.getNumber(), BUTTONS_TO_SHOW);
        modelAndView.addObject("allHotNewsList", allHotNewsList);
        modelAndView.addObject("selectedPageSize", evalPageSize);
        modelAndView.addObject("pageSizes", PAGE_SIZES);
        modelAndView.addObject("pager", pager);
        return modelAndView;
    }

    @RequestMapping("/recommend")
    public ModelAndView getRecommendNewsList(@RequestParam(value = "type", defaultValue = "金融科技") String type){
        ModelAndView modelAndView = new ModelAndView("detail");
        modelAndView.addObject("recommendNewsList", newsService.getRecommendNewsList(type));
        return modelAndView;
    }

    @RequestMapping(value = "/pdf", method = RequestMethod.GET)
    public StreamingResponseBody generatePdf(HttpServletResponse response, @RequestParam Integer id, Model model) throws IOException {
        News news = newsService.getNewsById(id);
        response.setContentType("application/pdf");
        response.setHeader("Content-Disposition", "attachment; filename=\"" + news.getId() + ".pdf\"");
        Base64 base64 = new Base64();
        InputStream inputStream = new ByteArrayInputStream(base64.decode(news.getPdf()));
        return outputStream -> {
            int nRead;
            byte[] data = new byte[1024];
            while ((nRead = inputStream.read(data, 0, data.length)) != -1) {
                outputStream.write(data, 0, nRead);
            }
        };
    }
}
