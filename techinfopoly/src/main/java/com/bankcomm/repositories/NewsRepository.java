package com.bankcomm.repositories;

import com.bankcomm.domain.News;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface NewsRepository extends PagingAndSortingRepository<News, String> {

    @Query(nativeQuery = true, name = "getAllByHot")
    Page<News> getAllByHot(Pageable pageable, @Param("hot") String hot);

    @Query(nativeQuery = true, name = "getTopHotNews")
    List<News> getTopHotNews();

    @Query(nativeQuery = true, name = "getAllByType")
    Page<News> getAllByType(Pageable pageable, @Param("type") String type);

    @Query(nativeQuery = true, name = "getRecommendNewsList")
    List<News> getRecommendNewsList(@Param("type") String type);

    Optional<News> findById(Integer id);
}
