package com.bankcomm.domain;

import javax.persistence.*;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;
import java.sql.Blob;
import java.util.Arrays;
import java.util.Base64;
import java.util.Date;

@Entity
@Table(name = "NEWS", schema = "SPIDER")
@SqlResultSetMappings(
        value = {
                @SqlResultSetMapping(
                        name="getAllByHot",
                        entities=@EntityResult(
                                entityClass=News.class,
                                fields={
                                        @FieldResult(name="id", column="id"),
                                        @FieldResult(name="url", column="url"),
                                        @FieldResult(name="title", column="title"),
                                        @FieldResult(name="content", column="content"),
                                        @FieldResult(name="cover", column="cover"),
                                        @FieldResult(name="pdf", column="pdf"),
                                        @FieldResult(name="type", column="type"),
                                        @FieldResult(name="keywords", column="keywords"),
                                        @FieldResult(name="hot", column="hot"),
                                        @FieldResult(name="update", column="update"),
                                        @FieldResult(name="batch", column="batch")
                                }
                        )
                ),
                @SqlResultSetMapping(
                        name="getTopHotNews",
                        entities=@EntityResult(
                                entityClass=News.class,
                                fields={
                                        @FieldResult(name="id", column="id"),
                                        @FieldResult(name="url", column="url"),
                                        @FieldResult(name="title", column="title"),
                                        @FieldResult(name="content", column="content"),
                                        @FieldResult(name="cover", column="cover"),
                                        @FieldResult(name="pdf", column="pdf"),
                                        @FieldResult(name="type", column="type"),
                                        @FieldResult(name="keywords", column="keywords"),
                                        @FieldResult(name="hot", column="hot"),
                                        @FieldResult(name="update", column="update"),
                                        @FieldResult(name="batch", column="batch")
                                }
                        )
                ),
                @SqlResultSetMapping(
                        name="getAllByType",
                        entities=@EntityResult(
                                entityClass=News.class,
                                fields={
                                        @FieldResult(name="id", column="id"),
                                        @FieldResult(name="url", column="url"),
                                        @FieldResult(name="title", column="title"),
                                        @FieldResult(name="content", column="content"),
                                        @FieldResult(name="cover", column="cover"),
                                        @FieldResult(name="pdf", column="pdf"),
                                        @FieldResult(name="type", column="type"),
                                        @FieldResult(name="keywords", column="keywords"),
                                        @FieldResult(name="hot", column="hot"),
                                        @FieldResult(name="update", column="update"),
                                        @FieldResult(name="batch", column="batch")
                                }
                        )
                ),
                @SqlResultSetMapping(
                        name="getRecommendNewsList",
                        entities=@EntityResult(
                                entityClass=News.class,
                                fields={
                                        @FieldResult(name="id", column="id"),
                                        @FieldResult(name="url", column="url"),
                                        @FieldResult(name="title", column="title"),
                                        @FieldResult(name="content", column="content"),
                                        @FieldResult(name="cover", column="cover"),
                                        @FieldResult(name="pdf", column="pdf"),
                                        @FieldResult(name="type", column="type"),
                                        @FieldResult(name="keywords", column="keywords"),
                                        @FieldResult(name="hot", column="hot"),
                                        @FieldResult(name="update", column="update"),
                                        @FieldResult(name="batch", column="batch")
                                }
                        )
                )
        }
)
@NamedNativeQueries(
        value = {
                @NamedNativeQuery(
                        name="getAllByHot",
                        query = "SELECT u.id, u.url, u.title, u.content, u.cover, null as pdf, u.type, u.keywords, u.hot, u.update, u.batch FROM News u WHERE u.hot = ?1",
                        resultClass = News.class,
                        resultSetMapping = "getAllByHot"
                ),
                @NamedNativeQuery(
                        name="getTopHotNews",
                        query = "SELECT u.id, u.url, u.title, u.content, u.cover, null as pdf, u.type, u.keywords, u.hot, u.update, u.batch FROM News u WHERE u.hot = '1' FETCH FIRST 20 ROWS ONLY",
                        resultClass = News.class,
                        resultSetMapping = "getTopHotNews"
                ),
                @NamedNativeQuery(
                        name="getAllByType",
                        query = "SELECT u.id, u.url, u.title, u.content, u.cover, null as pdf, u.type, u.keywords, u.hot, u.update, u.batch FROM News u WHERE u.type LIKE '%'||?1||'%'",
                        resultClass = News.class,
                        resultSetMapping = "getAllByType"
                ),
                @NamedNativeQuery(
                        name="getRecommendNewsList",
                        query = "SELECT u.id, u.url, u.title, u.content, u.cover, null as pdf, u.type, u.keywords, u.hot, u.update, u.batch FROM News u WHERE u.type LIKE '%'||?1||'%' FETCH FIRST 6 ROWS ONLY",
                        resultClass = News.class,
                        resultSetMapping = "getRecommendNewsList"
                ),
        }
)
@XmlRootElement
@XmlAccessorType(XmlAccessType.FIELD)
public class News  implements Serializable {
    @Id
    @Column()
    private Integer id;
    @Column()
    private String url;
    @Column()
    private String title;
    @Column()
    private String content;
    @Lob @Basic(fetch = FetchType.LAZY)
    @Column(name = "cover", columnDefinition="BLOB")
    private byte[] cover;
    @Lob @Basic(fetch = FetchType.LAZY)
    @Column(name = "pdf", columnDefinition="BLOB")
    private byte[] pdf;
    @Column()
    private String type;
    @Column()
    private String keywords;
    @Column()
    private String hot;
    @Column()
    private String update;
    @Column()
    private Date batch;

    public News() {
    }

    public News(Integer id, String url, String title, String content, byte[] cover, byte[] pdf, String type, String keywords, String hot, String update, Date batch) {
        this.id = id;
        this.url = url;
        this.title = title;
        this.content = content;
        this.cover = cover;
        this.pdf = pdf;
        this.type = type;
        this.keywords = keywords;
        this.hot = hot;
        this.update = update;
        this.batch = batch;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public byte[] getCover() {
        return cover;
    }

    public void setCover(byte[] cover) {
        this.cover = cover;
    }

    public byte[] getPdf() {
        return pdf;
    }

    public void setPdf(byte[] pdf) {
        this.pdf = pdf;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getKeywords() {
        return keywords;
    }

    public void setKeywords(String keywords) {
        this.keywords = keywords;
    }

    public String getHot() {
        return hot;
    }

    public void setHot(String hot) {
        this.hot = hot;
    }

    public String getUpdate() {
        return update;
    }

    public void setUpdate(String update) {
        this.update = update;
    }

    public Date getBatch() {
        return batch;
    }

    public void setBatch(Date batch) {
        this.batch = batch;
    }

    @Override
    public String toString() {
        return "News{" +
                "id=" + id +
                ", url='" + url + '\'' +
                ", title='" + title + '\'' +
                ", content='" + content + '\'' +
                ", cover=" + Arrays.toString(cover) +
                ", pdf=" + Arrays.toString(pdf) +
                ", type='" + type + '\'' +
                ", keywords='" + keywords + '\'' +
                ", hot='" + hot + '\'' +
                ", update='" + update + '\'' +
                ", batch=" + batch +
                '}';
    }
}
